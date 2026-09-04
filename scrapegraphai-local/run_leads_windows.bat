@echo off
REM Lance find_and_enrich_leads.py et journalise la sortie.
REM A MODIFIER : remplacez la ligne ci-dessous par le chemin reel du depot
REM "lead" sur votre machine (le dossier qui contient scrapegraphai-local\).
set LEAD_REPO=C:\Chemin\vers\lead

cd /d "%LEAD_REPO%\scrapegraphai-local\Scrapegraph-ai"
uv run python ..\find_and_enrich_leads.py >> "%LEAD_REPO%\scrapegraphai-local\logs\run_windows.log" 2>&1
