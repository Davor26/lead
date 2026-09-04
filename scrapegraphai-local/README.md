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

Le clonage du dépôt et `uv sync` (dépendances Python, depuis PyPI) ont donc réussi ici, mais
**l'installation d'Ollama, le téléchargement du modèle, `playwright install` (téléchargement des
navigateurs) et le test final sur `example.com` doivent être exécutés sur votre machine réelle**,
en suivant les étapes ci-dessous — votre machine n'a probablement pas cette restriction réseau.

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
| Playwright (binaires navigateurs) | Chromium/Firefox/WebKit | **échec ici** (CDN bloqué) — à relancer sur votre machine, voir §4 |
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

Il envoie le prompt *"Résume le contenu de la page et indique son titre principal."* sur
`https://example.com` et affiche le JSON résultat ainsi que les infos d'exécution
(tokens, coût — nul ici puisque 100% local).

## 6. Résultat attendu

`example.com` est une page statique très simple ("Example Domain"). Le résultat JSON doit
contenir un résumé mentionnant le titre `Example Domain` et le texte d'exemple de la page.
Aucune clé API n'est nécessaire : `graph_config` ne référence aucun `openai_api_key` ni service
payant, uniquement `base_url` vers l'instance Ollama locale.

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
