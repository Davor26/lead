# ScrapeGraphAI — installation locale (100% local, sans API payante)

Ce dossier contient une installation locale de [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai),
configurée pour tourner **entièrement en local avec Ollama**, sans clé API ni service payant.

## ⚠️ Important — où exécuter quoi

Ce dépôt Git a été préparé depuis une session Claude Code exécutée dans un **sandbox cloud
éphémère**, pas sur votre ordinateur. Ce sandbox a une politique réseau restrictive (uniquement
GitHub, PyPI, npm... autorisés) qui bloque plusieurs hôtes nécessaires :

- `ollama.com` / `registry.ollama.ai` / `huggingface.co` → impossible d'installer Ollama ou de
  télécharger un modèle depuis ce sandbox.
- `cdn.playwright.dev` / `playwright.download.prss.microsoft.com` → impossible de télécharger les
  binaires des navigateurs Playwright (Chromium) depuis ce sandbox, même si `playwright install`
  s'exécute (l'erreur observée est `403 request blocked: no rule or allowlist entry allows host`).

Même `https://example.com` (la cible du test) est bloqué depuis ce sandbox — la politique réseau
y est très restrictive (GitHub, PyPI, npm... seulement).

Le clonage du dépôt et `uv sync` (dépendances Python, depuis PyPI) ont donc réussi ici, et la
construction du graphe `SmartScraperGraph` a été validée localement (sans appel réseau). Mais
**l'installation d'Ollama, le téléchargement du modèle et le test final sur `example.com` doivent
être exécutés sur votre machine réelle**, en suivant les étapes ci-dessous — votre machine n'a
probablement pas cette restriction réseau.

**Correction (confirmée sur une exécution réelle) :** `SmartScraperGraph` (v2.2.2) ne transmet
**jamais** `use_soup` au nœud de récupération de page — voir `smart_scraper_graph.py`, où seuls
`llm_model`/`force`/`cut`/`loader_kwargs`/`browser_base`/`scrape_do`/`storage_state` sont passés au
`FetchNode`. Playwright est donc toujours nécessaire, même pour une page statique comme
`example.com`. **`uv run playwright install` (étape 4) est obligatoire avant l'étape 5.**

## Contenu du dossier

- `Scrapegraph-ai/` — dépôt officiel cloné en submodule Git, épinglé sur la version stable
  **v2.2.2** (dernière release au 2026-09-04, confirmée sur PyPI).
- `local_smartscraper_example.py` — script de test `SmartScraperGraph` configuré pour Ollama
  local, ciblant `https://example.com`.

## 1. Prérequis vérifiés

| Outil | Requis | Statut dans ce dépôt |
|---|---|---|
| Python | `>=3.12,<4.0` | `python3.12` / `python3.13` utilisés (`.python-version` = 3.12) |
| uv | dernière version | déjà installé (`uv 0.8.17` au moment de la préparation) |
| Dépendances Python (`scrapegraphai` 2.2.2, etc.) | — | installées via `uv sync` (réussi dans ce dépôt) |
| Playwright (binaires navigateurs) | Chromium/Firefox/WebKit | **échec ici** (CDN bloqué) — obligatoire, à relancer sur votre machine, voir §4 |
| Ollama | dernière version | **à installer sur votre machine**, voir §2 |

## 2. Installer Ollama (sur votre machine, pas dans ce sandbox)

Commande officielle (Linux, voir [ollama.com/download](https://ollama.com/download) pour
macOS/Windows) :

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

- macOS : télécharger l'app sur https://ollama.com/download/mac (ou `brew install ollama`).
- Windows : installeur sur https://ollama.com/download/windows.

Puis démarrer le service (généralement automatique après installation) :

```bash
ollama serve   # si non déjà lancé en arrière-plan / en tant que service
```

## 3. Choisir et télécharger le modèle

Vous avez indiqué **16 Go de RAM** sur votre machine. Modèle recommandé :

```bash
ollama pull llama3.1:8b
```

- Taille sur disque : ~4,9 Go (quantisation Q4_K_M par défaut).
- Bon compromis qualité d'extraction / vitesse sur CPU, contexte large (utile pour des pages
  HTML volumineuses), bien supporté par ScrapeGraphAI et Ollama.

Autres profils si besoin (RAM différente ou modèle à ajuster) :

| RAM disponible | Modèle conseillé | Commande |
|---|---|---|
| 8 Go | `qwen2.5:3b` ou `llama3.2:3b` | `ollama pull qwen2.5:3b` |
| 16 Go | `llama3.1:8b` (défaut retenu) | `ollama pull llama3.1:8b` |
| 32 Go+ | `qwen2.5:14b` | `ollama pull qwen2.5:14b` |

Alternative à qualité d'extraction structurée souvent meilleure sur 16 Go : `qwen2.5:7b-instruct`.

## 4. Installer les dépendances Python et Playwright

```bash
cd scrapegraphai-local/Scrapegraph-ai
uv sync
uv run playwright install
# Si des dépendances système manquent pour les navigateurs (Linux) :
uv run playwright install-deps
```

## 5. Lancer le test sur example.com

Depuis `scrapegraphai-local/`, avec le venv du submodule :

```bash
cd Scrapegraph-ai
uv run python ../local_smartscraper_example.py
```

Le script (`local_smartscraper_example.py`) utilise :

```python
graph_config = {
    "llm": {
        "model": "ollama/llama3.1:8b",
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
        "model_tokens": 8192,
    },
    "verbose": True,
    "headless": True,
}
```

Ce script a été validé sans réseau dans le sandbox (construction du graphe `SmartScraperGraph`,
3 nœuds : `Fetch` → `ParseNode` → `GenerateAnswer`), mais pas exécuté de bout en bout (Ollama et
`example.com` inaccessibles depuis ce sandbox). **Assurez-vous d'avoir lancé `uv run playwright
install` (étape 4) avant cette étape**, sinon vous aurez une erreur
`BrowserType.launch: Executable doesn't exist...`.

Il envoie le prompt *"Résume le contenu de la page et indique son titre principal."* sur
`https://example.com` et affiche le JSON résultat ainsi que les infos d'exécution
(tokens, coût — nul ici puisque 100% local).

## 6. Résultat obtenu (test réel, 2026-09-05)

Exécuté avec succès sur la machine Windows de l'utilisateur (`C:\Users\Home\Documents\lead`) :

```
Le titre principal de la page est "Example Domain" et le contenu est une description de ce
domaine, qui est utilisé pour les exemples de documentation sans nécessiter de permission.
```

- Modèle utilisé : `llama3.1:8b` via Ollama local (`http://localhost:11434`)
- Coût : `$0.0000` (aucune API payante, confirmé par les statistiques d'exécution)
- Temps total : 106s (Fetch 6s, ParseNode 7s, GenerateAnswer 93s)
- Le warning `None of the requested terms... appear in the parsed content` est inoffensif :
  `example.com` ne fait que 169 caractères, l'heuristique de pré-filtrage de ScrapeGraphAI ne
  trouve pas de correspondance exacte, mais le LLM lit et résume correctement la page malgré tout.

## 6bis. Résultat attendu (rappel, avant exécution)

`example.com` est une page statique très simple ("Example Domain"). Le résultat JSON doit
contenir un résumé mentionnant le titre `Example Domain` et le texte d'exemple de la page.
Aucune clé API n'est nécessaire : `graph_config` ne référence aucun `openai_api_key` ni service
payant, uniquement `base_url` vers l'instance Ollama locale.

## 7. Enrichir des leads (dirigeant / email / téléphone)

`../leads.csv` (à la racine du dépôt) contient des entreprises réelles trouvées via l'API
Pappers (nom, ville, secteur, SIREN, URL source) mais sans site web / dirigeant / email /
téléphone (non disponibles gratuitement).

`enrich_leads.py` complète ces champs pour chaque ligne :
1. Recherche du site officiel via DuckDuckGo (`scrapegraphai.utils.research_web.search_on_web`,
   gratuit, sans clé API), en écartant les annuaires/réseaux sociaux.
2. Scraping du site trouvé avec `SmartScraperGraph` (Ollama local) pour extraire dirigeant,
   email, téléphone.
3. Réécriture de `leads.csv` avec les résultats.

```bash
cd scrapegraphai-local/Scrapegraph-ai
uv run python ../enrich_leads.py
```

Comme pour le test `example.com`, ce script n'a pas pu être exécuté dans le sandbox cloud
(recherche web et sites cibles bloqués par la politique réseau) : script écrit et validé
syntaxiquement uniquement (`python -m py_compile` / import OK), à exécuter sur une machine avec
accès réseau complet.

## 8. Recherche + enrichissement réutilisable (`find_and_enrich_leads.py`)

Script réutilisable qui combine les étapes précédentes en une seule exécution, pensée pour
tourner régulièrement sans dupliquer de données :

- Recherche de nouvelles entreprises (< 50 salariés, Île-de-France, tous secteurs) via l'API
  publique **gratuite et sans clé** [recherche-entreprises.api.gouv.fr](https://recherche-entreprises.api.gouv.fr/)
  (remplace Pappers pour cette étape : pas de quota payant, aucune inscription).
- Ignore les entreprises déjà présentes dans `leads.csv` (par SIREN).
- Cherche le site officiel (DuckDuckGo, gratuit) puis extrait dirigeant/email/téléphone avec
  `SmartScraperGraph` + Ollama local, comme `enrich_leads.py`.
- N'ajoute que des lignes **nouvelles** à `leads.csv`, en dédupliquant par domaine de site web et
  par email par rapport à l'existant (jamais de doublon, jamais de ligne existante modifiée).
- Conserve `url_source` et ajoute une colonne `date_ajout` (date du jour, ISO `AAAA-MM-JJ`).
- Ralentit automatiquement (pause + nouvel essai, délai qui double à chaque échec) en cas de
  limitation (HTTP 429) ou d'erreur réseau sur l'API de recherche, DuckDuckGo ou le scraping.
- Journalise clairement chaque étape et chaque erreur dans `scrapegraphai-local/logs/leads.log`
  (fichier + affichage console).

### Commande pour le lancer manuellement

```bash
cd scrapegraphai-local/Scrapegraph-ai
uv run python ../find_and_enrich_leads.py
```

Validé dans le sandbox : syntaxe, chargement du module, logique de sauvegarde/déduplication
(test avec un `leads.csv` temporaire). La recherche d'entreprises et le scraping n'ont pas pu être
testés de bout en bout ici (réseau bloqué, comme documenté plus haut) — à vérifier lors de la
première exécution manuelle sur votre machine avant d'activer l'automatisation ci-dessous.

### Exécution automatique chaque matin à 8h (Windows) — non activée

Fichiers préparés, **rien n'est activé** :

- `scrapegraphai-local/run_leads_windows.bat` : lance le script et journalise la sortie dans
  `scrapegraphai-local/logs/run_windows.log`. Déjà configuré avec votre chemin réel
  (`C:\Users\Home\Documents\lead`).

Commande exacte pour créer la tâche planifiée (à exécuter vous-même dans une invite de commandes) :

```bat
schtasks /Create /TN "Leads ScrapeGraphAI IDF" /TR "\"C:\Users\Home\Documents\lead\scrapegraphai-local\run_leads_windows.bat\"" /SC DAILY /ST 08:00 /F
```

- `/TN` : nom de la tâche dans le Planificateur de tâches Windows.
- `/TR` : chemin complet vers `run_leads_windows.bat` (à adapter à votre chemin réel).
- `/SC DAILY /ST 08:00` : exécution quotidienne à 8h00, heure de la machine.
- `/F` : force la création même si une tâche du même nom existe déjà.

Pour supprimer la tâche ensuite : `schtasks /Delete /TN "Leads ScrapeGraphAI IDF" /F`.

**Cette commande n'a pas été exécutée** : je n'ai pas accès à votre machine Windows depuis ce
sandbox cloud. Lancez-la vous-même seulement après avoir testé la commande manuelle ci-dessus au
moins une fois avec succès et vérifié le chemin dans `run_leads_windows.bat`.

## Pourquoi un submodule Git plutôt qu'un simple `pip install` ?

La demande initiale demandait de cloner le dépôt officiel puis d'exécuter `uv sync` +
`uv run playwright install`, ce qui correspond au workflow de développement documenté dans le
`README.md` du dépôt ScrapeGraphAI (pas seulement `pip install scrapegraphai`). Un submodule Git
permet de garder le code source du dépôt tiers, épinglé à une version précise (`v2.2.2`), sans le
dupliquer dans l'historique de ce dépôt.

Pour cloner ce dépôt avec le submodule inclus :

```bash
git clone --recurse-submodules <url-du-repo>
# ou, si déjà cloné :
git submodule update --init --recursive
```
