"""
Test local de SmartScraperGraph (ScrapeGraphAI) avec un modèle Ollama local.

Aucune clé API, aucun service payant : le LLM tourne entièrement en local via
Ollama (http://localhost:11434). Voir README.md dans ce dossier pour
l'installation d'Ollama et le téléchargement du modèle.

Usage:
    uv run --project Scrapegraph-ai python ../local_smartscraper_example.py
    (ou, une fois le venv du submodule activé)
    python local_smartscraper_example.py
"""

import json

from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info

# Modèle recommandé pour une machine avec ~16 Go de RAM, sans GPU dédié.
# Adapter selon la RAM disponible :
#   8 Go  -> "ollama/qwen2.5:3b" ou "ollama/llama3.2:3b"
#   16 Go -> "ollama/llama3.1:8b" (défaut ci-dessous)
#   32 Go+ -> "ollama/qwen2.5:14b"
OLLAMA_MODEL = "ollama/llama3.1:8b"

graph_config = {
    "llm": {
        "model": OLLAMA_MODEL,
        "temperature": 0,
        "format": "json",
        "base_url": "http://localhost:11434",
        "model_tokens": 8192,
    },
    "verbose": True,
    "headless": True,
    # NB : SmartScraperGraph (v2.2.2) ne transmet pas "use_soup" au nœud de
    # récupération de page (voir smart_scraper_graph.py, FetchNode reçoit
    # seulement llm_model/force/cut/loader_kwargs/browser_base/scrape_do/
    # storage_state) : Playwright est toujours utilisé pour aller chercher la
    # page, même sur une page statique comme example.com. Il faut donc avoir
    # lancé `uv run playwright install` avant d'exécuter ce script.
}

smart_scraper_graph = SmartScraperGraph(
    prompt="Résume le contenu de la page et indique son titre principal.",
    source="https://example.com",
    config=graph_config,
)

if __name__ == "__main__":
    result = smart_scraper_graph.run()
    print(json.dumps(result, indent=4, ensure_ascii=False))

    graph_exec_info = smart_scraper_graph.get_execution_info()
    print(prettify_exec_info(graph_exec_info))
