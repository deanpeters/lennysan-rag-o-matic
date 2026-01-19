# v0.75 - Web Search Fallback 🌐

**Release Date:** January 19, 2026  
**Status:** Mac-only, CLI-only, Serper web fallback

v0.75 adds one focused capability: **optional web search fallback** when the corpus can’t answer a query.

## What’s New (One Feature)

### ✅ Web Search Fallback
- `--web-search on|off|always`
- AUTO mode: runs only when the direct answer is weak
- ALWAYS mode: force a web lookup for testing
- Web sources are shown as `[title](URL)` links

## Important Notes

- AUTO mode is **intentionally conservative** to avoid unnecessary API calls.
- If you want to test web search behavior, use `--web-search always`.
- To avoid burning Serper quota while tuning heuristics, test logic in a chatbot first and only then codify it.

## API Key

Set in your shell:

```bash
export SERPER_API_KEY="your-key"
```

If the key is missing, web search is automatically disabled with a warning.

## What Didn’t Change

- YAML metadata preservation end‑to‑end
- Source attribution formatting
- Local embeddings + ChromaDB
- Mac‑only CLI workflow

## What This Is NOT (Yet)

- ❌ Docker/SearXNG fallback (planned v0.8)
- ❌ explore.py diagnostic logs in logs/ (planned v0.9)
- ❌ Jupyter notebooks (v1.0)
- ❌ Streamlit UI (v2.0)
- ❌ Windows support (v3.0)

## Philosophy Reminder

**One feature per version.** v0.75 is web search fallback only.
