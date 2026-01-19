# v0.75 - Web Search Fallback

Release date: 2026-01-19

This release adds one focused capability: optional web search fallback when the
corpus cannot answer a query.

## Highlights
- Web search fallback with `--web-search on|off|always`
- AUTO mode is conservative and only triggers when direct answers are weak
- ALWAYS mode forces a web lookup for testing
- Web sources are listed as links in the Sources section

## How to use
1) Set your SERPER API key:

```bash
export SERPER_API_KEY="your-key"
```

2) Run a query with fallback enabled:

```bash
python explore.py --web-search on "why safe sucks"
```

To force a search on every query (for testing):

```bash
python explore.py --web-search always "why safe sucks"
```

## Notes
- If the API key is missing, web search is disabled with a warning.
- AUTO mode is intentionally conservative to protect quota and cost.
- This release does not change attribution, metadata preservation, or the
  CLI-first workflow.

## Not included
- Docker/SearXNG fallback (planned v0.8)
- explore.py diagnostic logs in logs/ (planned v0.9)
- Jupyter notebooks (v1.0)
- Streamlit UI (v2.0)
- Windows support (v3.0)
