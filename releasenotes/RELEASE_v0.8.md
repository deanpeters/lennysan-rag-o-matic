# v0.8 - Docker Search Option 🐳

**Release Date:** January 21, 2026  
**Status:** Mac-only, CLI-only, Docker optional

v0.8 adds one focused capability: **an optional Docker search backend** for people who want local, open-source search instead of an external API.

## What’s New (One Feature)

### ✅ Docker Search Option (SearXNG)
- One-button script: `scripts/docker_search.sh`
- Optional local search provider via SearXNG
- CLI override: `--web-provider docker`
- Port override: `SEARXNG_PORT=8081` if 8080 is taken

## Quick Start (Docker Path)

```bash
chmod +x scripts/docker_search.sh
./scripts/docker_search.sh "why safe sucks"
```

If port 8080 is already used:

```bash
SEARXNG_PORT=8081 ./scripts/docker_search.sh "why safe sucks"
```

## Important Notes

- Docker is powerful but fussy. If it gets weird, use the nuclear reset:
  ```bash
  docker rm -f searxng
  rm -f logs/searxng.settings.yml
  ./scripts/docker_search.sh "test query"
  ```
- API search is still available and recommended for most people who want speed over setup.
- Web search defaults to AUTO mode; use `--web-search always` for testing.

## What Didn’t Change

- YAML metadata preservation end-to-end
- Source attribution formatting
- Local embeddings + ChromaDB
- Mac-only CLI workflow

## What This Is NOT (Yet)

- ❌ Dean-i-fried response mode (planned v0.85)
- ❌ explore.py diagnostic logs in logs/ (planned v0.9)
- ❌ Jupyter notebooks (v1.0)
- ❌ Streamlit UI (v2.0)
- ❌ Windows support (v3.0)

## Philosophy Reminder

**One feature per version.** v0.8 is Docker search only.
