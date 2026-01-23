# CONFIGS.yaml (v0.6) - Draft Schema + Example

Goal: a **human‑readable, extensible** config that can grow with new providers, models,
corpora, and notebook topics. CLI flags always override config values.

---

## Design Principles

- **Readable first**: PMs should understand and edit it without fear.
- **Extensible**: new providers/models/corpora should slot in cleanly.
- **Single source of defaults**: no hidden magic.
- **Future‑proof**: add notebooks, web fallback, multi‑corpus later without breaking.

---

## Draft Schema (sections)

Top‑level sections are grouped by concept instead of by implementation detail:

- `version`: config schema version string
- `defaults`: default model/provider + behavior defaults
- `providers`: API provider registry (API key env vars, display names)
- `models`: model registry (provider + model id + status)
- `paths`: file system paths (vector DB, corpora, topic index, notebooks)
- `retrieval`: RAG retrieval behavior (k, fetch_k, search type)
- `output`: formatting rules (max sources, response format)
- `features`: feature flags (future web fallback, notebooks, etc.)

---

## Example CONFIGS.yaml

```yaml
version: "0.6"

# Defaults for CLI when no flags are provided
defaults:
  provider: "anthropic"
  model: "haiku"
  response_format: "direct_inferred_missing"
  verbose: true

# Provider registry (future‑proof for more APIs)
providers:
  anthropic:
    api_key_env: "ANTHROPIC_API_KEY"
    display_name: "Anthropic"
  openai:
    api_key_env: "OPENAI_API_KEY"
    display_name: "OpenAI"
  # Example placeholder for future providers
  # gemini:
  #   api_key_env: "GOOGLE_API_KEY"
  #   display_name: "Google"

# Model registry (human‑friendly aliases)
models:
  haiku:
    provider: "anthropic"
    id: "claude-haiku-4-5-20251001"
    label: "Claude Haiku 4.5 (cheapest)"
    status: "active"
  sonnet-4:
    provider: "anthropic"
    id: "claude-sonnet-4-20250514"
    label: "Claude Sonnet 4 (balanced)"
    status: "active"
  gpt-4o-mini:
    provider: "openai"
    id: "gpt-4o-mini"
    label: "GPT-4o mini (cheapest OpenAI)"
    status: "active"
  gpt-4o:
    provider: "openai"
    id: "gpt-4o"
    label: "GPT-4o (quality OpenAI)"
    status: "active"

# Filesystem paths
paths:
  vector_db: "data/chroma_db"
  logs: "logs"
  corpora:
    - name: "lenny"
      path: "episodes"
  topic_index:
    path: "index"
  notebooks:
    root: "notebooks"
    topics_root: "notebooks/topics"

# Retrieval defaults
retrieval:
  search_type: "mmr"
  k: 8
  fetch_k: 24

# Output formatting
output:
  max_sources: 3
  response_format: "direct_inferred_missing"

# Feature flags (future‑safe, off by default)
features:
  web_search: true
  notebooks: false

web_search:
  # Requires SERPER_API_KEY for api, or Docker/SearXNG running for docker.
  mode: "on"
  provider: "api"  # api | docker
  endpoint: "https://google.serper.dev/search"
  docker_endpoint: "http://localhost:8080/search"
  allow_api_fallback: false
  api_key_env: "SERPER_API_KEY"
  max_results: 5
  timeout_sec: 10
```

---

## Notes for v0.6

- **CLI overrides config** (e.g., `--model sonnet-4` wins over defaults).
- This layout scales when we add new providers or multiple corpora.
- Notebook paths are declared now for clarity, even if notebooks are v1.0.
