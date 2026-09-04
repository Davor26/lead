"""
Enrichissement de leads.csv avec ScrapeGraphAI + Ollama, 100% local et gratuit.

Pour chaque entreprise du fichier ../leads.csv (nom, ville déjà connus via Pappers) :
  1. Recherche le site web officiel avec une recherche DuckDuckGo gratuite,
     sans clé API (scrapegraphai.utils.research_web.search_on_web), en
     écartant les annuaires/réseaux sociaux.
  2. Scrape ce site avec SmartScraperGraph (LLM Ollama local) pour en extraire
     dirigeant, email et téléphone.
  3. Met à jour leads.csv avec les résultats trouvés.

Prérequis : voir README.md dans ce dossier (Ollama installé, modèle téléchargé,
`uv sync` déjà fait dans Scrapegraph-ai/).

Usage (depuis scrapegraphai-local/Scrapegraph-ai/) :
    uv run python ../enrich_leads.py
"""

import csv
import time
from pathlib import Path

from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils.research_web import search_on_web

LEADS_CSV = Path(__file__).parent / "leads.csv"

# Mêmes réglages que local_smartscraper_example.py — voir README.md pour
# adapter le modèle à la RAM disponible.
OLLAMA_MODEL = "ollama/llama3.1:8b"

LLM_CONFIG = {
    "model": OLLAMA_MODEL,
    "temperature": 0,
    "format": "json",
    "base_url": "http://localhost:11434",
    "model_tokens": 8192,
}

# Annuaires / réseaux sociaux à ignorer dans les résultats de recherche :
# ce ne sont pas les sites officiels des entreprises.
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
    "maps.app.goo.gl",
)


def trouver_site_officiel(nom_entreprise: str, ville: str) -> str | None:
    """Cherche le site officiel d'une entreprise via une recherche web gratuite."""
    requete = f"{nom_entreprise} {ville} site officiel"
    try:
        resultats = search_on_web(
            query=requete, search_engine="duckduckgo", max_results=8, language="fr"
        )
    except Exception as exc:
        print(f"  Recherche échouée pour {nom_entreprise!r} : {exc}")
        return None

    for url in resultats:
        domaine = url.split("/")[2].lower() if "://" in url else url.lower()
        if not any(exclu in domaine for exclu in DOMAINES_EXCLUS):
            return url
    return None


def extraire_contact(url: str) -> dict:
    """Scrape une page avec SmartScraperGraph (Ollama local) pour en extraire le contact."""
    graph_config = {
        "llm": LLM_CONFIG,
        "verbose": False,
        "headless": True,
        # Certains sites nécessitent du JS : si use_soup échoue ou ne trouve
        # rien, relancer avec "use_soup": False et `uv run playwright install`.
        "use_soup": True,
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
        resultat = graph.run()
    except Exception as exc:
        print(f"  Scraping échoué pour {url} : {exc}")
        return {"dirigeant": "", "email": "", "telephone": ""}

    return {
        "dirigeant": resultat.get("dirigeant", "") or "",
        "email": resultat.get("email", "") or "",
        "telephone": resultat.get("telephone", "") or "",
    }


def main() -> None:
    with LEADS_CSV.open(encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))

    for i, ligne in enumerate(lignes, start=1):
        nom = ligne["nom"]
        ville = ligne["ville"]
        print(f"[{i}/{len(lignes)}] {nom} ({ville})")

        site = trouver_site_officiel(nom, ville)
        if not site:
            print("  Aucun site officiel trouvé.")
            continue

        ligne["site_web"] = site
        print(f"  Site trouvé : {site}")

        contact = extraire_contact(site)
        ligne["dirigeant"] = contact["dirigeant"]
        ligne["email"] = contact["email"]
        ligne["telephone"] = contact["telephone"]
        print(f"  Contact extrait : {contact}")

        # Petite pause pour rester raisonnable vis-à-vis des sites scrapés.
        time.sleep(1)

    champs = list(lignes[0].keys())
    with LEADS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)

    print(f"\nTerminé. {LEADS_CSV} mis à jour avec {len(lignes)} entreprises.")


if __name__ == "__main__":
    main()
