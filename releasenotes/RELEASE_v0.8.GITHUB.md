# v0.8 - Docker Search Option

Release date: 2026-01-21

This release adds one focused capability: an optional Docker search backend
(SearXNG) for local, open-source web search.

## Highlights
- One-button Docker script: `scripts/docker_search.sh`
- Optional local SearXNG provider (`--web-provider docker`)
- Port override via `SEARXNG_PORT=8081`
- Web search remains AUTO by default; use `--web-search always` for testing

## How to use
1) Start Docker Desktop (macOS: `open -a Docker`)

2) Run the one-button script:

```bash
chmod +x scripts/docker_search.sh
./scripts/docker_search.sh "why safe sucks"
```

If port 8080 is taken:

```bash
SEARXNG_PORT=8081 ./scripts/docker_search.sh "why safe sucks"
```

## Notes
- If Docker gets stuck, do a nuclear reset:
  ```bash
  docker rm -f searxng
  rm -f logs/searxng.settings.yml
  ./scripts/docker_search.sh "test query"
  ```
- API search is still supported and recommended for most users who want speed.
- This release does not change attribution, metadata preservation, or the
  CLI-first workflow.

## Not included
- Dean-i-fried response mode (planned v0.85)
- explore.py diagnostic logs in logs/ (planned v0.9)
- Jupyter notebooks (v1.0)
- Streamlit UI (v2.0)
- Windows support (v3.0)
