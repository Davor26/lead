"""
Recherche + enrichissement de leads, en local, gratuit, réutilisable.

À chaque exécution :
  1. Cherche de nouvelles entreprises (< 50 salariés, Île-de-France, tous secteurs)
     via l'API publique gratuite recherche-entreprises.api.gouv.fr (aucune clé,
     aucune inscription).
  2. Ignore les entreprises déjà présentes dans leads.csv (par SIREN).
  3. Pour chaque nouvelle entreprise : cherche son site officiel (DuckDuckGo,
     gratuit) puis scrape dirigeant/email/téléphone avec SmartScraperGraph
     (Ollama local).
  4. Ajoute les nouvelles lignes à leads.csv, en dédupliquant par domaine de
     site web et par email par rapport à l'existant.
  5. Ralentit automatiquement (backoff exponentiel) en cas de limitation
     (HTTP 429 ou erreurs réseau) sur l'API de recherche, DuckDuckGo ou le
     scraping.
  6. Journalise clairement les erreurs dans logs/leads.log.

Ne modifie jamais les lignes déjà présentes : seuls des ajouts sont possibles.

Usage manuel (depuis scrapegraphai-local/Scrapegraph-ai/) :
    uv run python ../find_and_enrich_leads.py

Voir README.md pour la configuration de l'exécution automatique quotidienne.
"""

from __future__ import annotations

import csv
import logging
import random
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils.research_web import search_on_web

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV = REPO_ROOT / "leads.csv"
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "leads.log"

CHAMPS = [
    "nom",
    "site_web",
    "ville",
    "dirigeant",
    "email",
    "telephone",
    "url_source",
    "secteur",
    "siren",
    "date_ajout",
]

# Critères de recherche : < 50 salariés, Île-de-France, tous secteurs.
# Codes tranche_effectif_salarie INSEE pour "moins de 50 salariés".
TRANCHES_EFFECTIF = ["00", "01", "02", "03", "11", "12"]
DEPARTEMENTS_IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]

NB_NOUVELLES_ENTREPRISES_PAR_EXECUTION = 20
API_RECHERCHE_ENTREPRISES = "https://recherche-entreprises.api.gouv.fr/search"

OLLAMA_MODEL = "ollama/llama3.1:8b"
LLM_CONFIG = {
    "model": OLLAMA_MODEL,
    "temperature": 0,
    "format": "json",
    "base_url": "http://localhost:11434",
    "model_tokens": 8192,
}

DOMAINES_EXCLUS = (
    "pappers.fr",
    "societe.com",
    "infogreffe.fr",
    "verif.com",
    "manageo.fr",
    "kompass.com",
    "pagesjaunes.fr",
    "societeinfo.com",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "indeed.com",
    "glassdoor.fr",
    "wikipedia.org",
    "google.com",
    "recherche-entreprises.api.gouv.fr",
    "annuaire-entreprises.data.gouv.fr",
    "maps.app.goo.gl",
)

# ---------------------------------------------------------------------------
# Journalisation
# ---------------------------------------------------------------------------

LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("leads")
logger.setLevel(logging.INFO)
logger.handlers.clear()

_formatteur = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

_handler_fichier = logging.FileHandler(LOG_FILE, encoding="utf-8")
_handler_fichier.setFormatter(_formatteur)
_handler_fichier.setLevel(logging.INFO)
logger.addHandler(_handler_fichier)

_handler_console = logging.StreamHandler()
_handler_console.setFormatter(logging.Formatter("%(message)s"))
_handler_console.setLevel(logging.INFO)
logger.addHandler(_handler_console)


# ---------------------------------------------------------------------------
# Ralentissement automatique (backoff exponentiel)
# ---------------------------------------------------------------------------


def avec_backoff(fonction, *args, max_tentatives=5, delai_initial=2.0, contexte="", **kwargs):
    """Appelle `fonction` en ralentissant automatiquement en cas de erreur
    réseau ou de limitation (HTTP 429). Relance l'exception d'origine si
    toutes les tentatives échouent."""
    delai = delai_initial
    for tentative in range(1, max_tentatives + 1):
        try:
            return fonction(*args, **kwargs)
        except requests.exceptions.HTTPError as exc:
            statut = getattr(exc.response, "status_code", None)
            if statut == 429 or (statut and 500 <= statut < 600):
                logger.warning(
                    "%s : limitation/erreur serveur (HTTP %s), tentative %d/%d, "
                    "pause de %.1fs",
                    contexte, statut, tentative, max_tentatives, delai,
                )
            else:
                raise
        except (requests.exceptions.RequestException, TimeoutError) as exc:
            logger.warning(
                "%s : erreur réseau (%s), tentative %d/%d, pause de %.1fs",
                contexte, exc, tentative, max_tentatives, delai,
            )
        if tentative == max_tentatives:
            break
        time.sleep(delai + random.uniform(0, 1))
        delai *= 2
    raise RuntimeError(f"{contexte} : échec après {max_tentatives} tentatives")


# ---------------------------------------------------------------------------
# Étape 1 : recherche de nouvelles entreprises (API publique gratuite)
# ---------------------------------------------------------------------------


@dataclass
class Candidat:
    siren: str
    nom: str
    ville: str
    secteur: str
    url_source: str = field(default="")


def _appel_api_recherche(departement: str, tranche_effectif: str, page: int) -> dict:
    reponse = requests.get(
        API_RECHERCHE_ENTREPRISES,
        params={
            "departement": departement,
            "tranche_effectif_salarie": tranche_effectif,
            "etat_administratif": "A",
            "page": page,
            "per_page": 25,
        },
        timeout=15,
    )
    reponse.raise_for_status()
    return reponse.json()


def rechercher_nouvelles_entreprises(sirens_deja_connus: set[str], limite: int) -> list[Candidat]:
    """Parcourt l'API publique jusqu'à trouver `limite` entreprises dont le
    SIREN n'est pas déjà dans leads.csv."""
    candidats: list[Candidat] = []
    vus_cette_execution: set[str] = set()

    for departement in DEPARTEMENTS_IDF:
        for tranche in TRANCHES_EFFECTIF:
            page = 1
            while len(candidats) < limite:
                try:
                    data = avec_backoff(
                        _appel_api_recherche,
                        departement,
                        tranche,
                        page,
                        contexte=f"Recherche API (dept={departement}, tranche={tranche}, page={page})",
                    )
                except Exception:
                    logger.exception(
                        "Échec définitif de la recherche pour dept=%s tranche=%s page=%s",
                        departement, tranche, page,
                    )
                    break

                resultats = data.get("results", [])
                if not resultats:
                    break

                for entreprise in resultats:
                    siren = entreprise.get("siren", "")
                    if not siren or siren in sirens_deja_connus or siren in vus_cette_execution:
                        continue
                    vus_cette_execution.add(siren)

                    siege = entreprise.get("siege", {}) or {}
                    ville = siege.get("libelle_commune", "") or ""
                    code_postal = siege.get("code_postal", "") or ""
                    ville_affichee = f"{ville} ({code_postal})" if code_postal else ville

                    candidats.append(
                        Candidat(
                            siren=siren,
                            nom=entreprise.get("nom_complet")
                            or entreprise.get("nom_raison_sociale")
                            or siren,
                            ville=ville_affichee,
                            secteur=entreprise.get("libelle_activite_principale", "") or "",
                            url_source=f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}",
                        )
                    )
                    if len(candidats) >= limite:
                        break

                page += 1
                if page > 20:  # garde-fou anti-boucle infinie
                    break

            if len(candidats) >= limite:
                break
        if len(candidats) >= limite:
            break

    return candidats


# ---------------------------------------------------------------------------
# Étape 2 : enrichissement (site web + dirigeant/email/téléphone)
# ---------------------------------------------------------------------------


def trouver_site_officiel(nom_entreprise: str, ville: str) -> str | None:
    requete = f"{nom_entreprise} {ville} site officiel"
    try:
        resultats = avec_backoff(
            search_on_web,
            query=requete,
            search_engine="duckduckgo",
            max_results=8,
            language="fr",
            contexte=f"Recherche du site officiel de {nom_entreprise!r}",
        )
    except Exception:
        logger.exception("Recherche de site officiel échouée pour %r", nom_entreprise)
        return None

    for url in resultats:
        domaine = urlparse(url).netloc.lower()
        if domaine and not any(exclu in domaine for exclu in DOMAINES_EXCLUS):
            return url
    return None


def extraire_contact(url: str) -> dict:
    graph_config = {
        "llm": LLM_CONFIG,
        "verbose": False,
        "headless": True,
    }
    prompt = (
        "Cherche sur cette page les informations de contact de l'entreprise : "
        "le nom du dirigeant (gérant, président ou PDG), une adresse email de "
        "contact, et un numéro de téléphone. Réponds uniquement avec un JSON "
        'de la forme {"dirigeant": "...", "email": "...", "telephone": "..."}. '
        "Mets une chaîne vide si une information est introuvable."
    )
    try:
        graph = SmartScraperGraph(prompt=prompt, source=url, config=graph_config)
        resultat = avec_backoff(graph.run, contexte=f"Scraping de {url}")
    except Exception:
        logger.exception("Scraping échoué pour %s", url)
        return {"dirigeant": "", "email": "", "telephone": ""}

    return {
        "dirigeant": (resultat or {}).get("dirigeant", "") or "",
        "email": (resultat or {}).get("email", "") or "",
        "telephone": (resultat or {}).get("telephone", "") or "",
    }


def domaine_de(url: str) -> str:
    if not url:
        return ""
    netloc = urlparse(url).netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


# ---------------------------------------------------------------------------
# Étape 3 : lecture / écriture de leads.csv avec déduplication
# ---------------------------------------------------------------------------


def charger_leads_existants() -> list[dict]:
    if not LEADS_CSV.exists():
        return []
    with LEADS_CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sauvegarder_leads(lignes: list[dict]) -> None:
    fichier_temporaire = LEADS_CSV.with_suffix(".csv.tmp")
    with fichier_temporaire.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS)
        writer.writeheader()
        for ligne in lignes:
            writer.writerow({champ: ligne.get(champ, "") for champ in CHAMPS})
    fichier_temporaire.replace(LEADS_CSV)


def main() -> None:
    logger.info("=== Démarrage de la recherche/enrichissement de leads ===")

    leads_existants = charger_leads_existants()
    sirens_connus = {ligne["siren"] for ligne in leads_existants if ligne.get("siren")}
    domaines_connus = {
        domaine_de(ligne.get("site_web", "")) for ligne in leads_existants
    } - {""}
    emails_connus = {
        (ligne.get("email") or "").strip().lower() for ligne in leads_existants
    } - {""}

    logger.info(
        "%d leads déjà en base (leads.csv). Recherche de %d nouvelles entreprises...",
        len(leads_existants), NB_NOUVELLES_ENTREPRISES_PAR_EXECUTION,
    )

    candidats = rechercher_nouvelles_entreprises(
        sirens_connus, NB_NOUVELLES_ENTREPRISES_PAR_EXECUTION
    )
    logger.info("%d nouvelles entreprises candidates trouvées.", len(candidats))

    nouvelles_lignes = []
    for i, candidat in enumerate(candidats, start=1):
        logger.info("[%d/%d] %s (%s)", i, len(candidats), candidat.nom, candidat.ville)

        site = trouver_site_officiel(candidat.nom, candidat.ville)
        contact = {"dirigeant": "", "email": "", "telephone": ""}
        if site:
            domaine = domaine_de(site)
            if domaine in domaines_connus:
                logger.info("  Domaine %s déjà présent dans leads.csv, ignoré.", domaine)
                site = None
            else:
                logger.info("  Site trouvé : %s", site)
                contact = extraire_contact(site)
        else:
            logger.info("  Aucun site officiel trouvé.")

        email_normalise = (contact["email"] or "").strip().lower()
        if email_normalise and email_normalise in emails_connus:
            logger.info("  Email %s déjà présent dans leads.csv, contact ignoré.", email_normalise)
            contact = {"dirigeant": "", "email": "", "telephone": ""}
            email_normalise = ""

        nouvelles_lignes.append(
            {
                "nom": candidat.nom,
                "site_web": site or "",
                "ville": candidat.ville,
                "dirigeant": contact["dirigeant"],
                "email": contact["email"],
                "telephone": contact["telephone"],
                "url_source": candidat.url_source,
                "secteur": candidat.secteur,
                "siren": candidat.siren,
                "date_ajout": date.today().isoformat(),
            }
        )
        if site:
            domaines_connus.add(domaine_de(site))
        if email_normalise:
            emails_connus.add(email_normalise)

        time.sleep(1)  # pause raisonnable entre entreprises

    sauvegarder_leads(leads_existants + nouvelles_lignes)
    logger.info(
        "=== Terminé : %d nouvelles lignes ajoutées, %d au total dans %s ===",
        len(nouvelles_lignes), len(leads_existants) + len(nouvelles_lignes), LEADS_CSV,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Échec non récupéré de l'exécution")
        raise
