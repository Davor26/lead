@echo off
REM Lance find_and_enrich_leads.py et journalise la sortie.
set LEAD_REPO=C:\Users\Home\Documents\lead

cd /d "%LEAD_REPO%\scrapegraphai-local\Scrapegraph-ai"
uv run python ..\find_and_enrich_leads.py >> "%LEAD_REPO%\scrapegraphai-local\logs\run_windows.log" 2>&1
