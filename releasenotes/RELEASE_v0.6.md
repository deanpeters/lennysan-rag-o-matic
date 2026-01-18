# v0.6 - CONFIGS.yaml 🧭

**Release Date:** January 18, 2026  
**Status:** Mac-only, CLI-only, CONFIGS.yaml added

v0.6 adds one focused capability: **a human‑readable CONFIGS.yaml** for defaults and paths.
CLI flags always override config values.

## What’s New (One Feature)

### ✅ CONFIGS.yaml
- Central place for model defaults, providers, and paths
- Extensible layout for future corpora and notebooks
- Retrieval defaults live in config (k, fetch_k, search_type)

## Example

```yaml
defaults:
  model: "haiku"

paths:
  vector_db: "data/chroma_db"

retrieval:
  search_type: "mmr"
  k: 8
  fetch_k: 24
```

## What Didn’t Change

- YAML metadata preservation end‑to‑end
- Source attribution formatting
- Local embeddings + ChromaDB
- Mac‑only CLI workflow

## What This Is NOT (Yet)

- ❌ Web search fallback (v0.75)
- ❌ Jupyter notebooks (v1.0)
- ❌ Streamlit UI (v2.0)
- ❌ Windows support (v3.0)

## Philosophy Reminder

**One feature per version.** v0.6 is CONFIGS.yaml only.

