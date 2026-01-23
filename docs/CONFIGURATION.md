# Configuration (CONFIGS.yaml)

`CONFIGS.yaml` is the single source of truth for defaults, which means you can change how the tool behaves without touching the code. Think “product settings,” not “developer surgery.”

CLI flags can override those defaults for a single run, but the baseline values live here. If you want the repo to behave consistently every time you use it, this is the file you edit.

## Overview

`CONFIGS.yaml` is where you put the repo on rails.

Think of it as the difference between:
- “This tool works if I remember twelve flags”
- and “This tool behaves the way I want by default”

If you are doing real research, you want consistency. You want the same model, the same retrieval behavior, the same citation output, and the same safety rules every time you run a query. Not because you are boring. Because you are trying to learn, compare results, and trust what you’re seeing.

This file is also your cheapest way to experiment without turning your repo into a Franken-script. Want a different default model? Want fewer retrieved chunks? Want web search to be AUTO instead of ALWAYS? Want to keep output quiet unless you are debugging? That’s config work, not code work.

CLI flags still matter. They are your “one-off override” tool for quick experiments. But [CONFIGS.yaml](CONFIGS.yaml) is where you set the baseline for how you work when you are not actively thinking about flags, which is… most of the time.

If you only read one thing before you start tweaking knobs, read this: treat `CONFIGS.yaml` like product defaults. Change it deliberately. Change one thing at a time. Then run the same query twice and see what actually changed.

---

## Example

```yaml
defaults:
  model: "haiku"  # haiku | sonnet-4 | gpt-4o-mini | gpt-4o
  verbose: true

paths:
  vector_db: "data/chroma_db"

retrieval:
  search_type: "mmr"
  k: 8
  fetch_k: 24

features:
  web_search: true

web_search:
  # Requires SERPER_API_KEY for api, or Docker/SearXNG running for docker.
  mode: "on"   # on | off | always
  provider: "api"  # api | docker
  endpoint: "https://google.serper.dev/search"
  docker_endpoint: "http://localhost:8080/search"
  allow_api_fallback: false
  api_key_env: "SERPER_API_KEY"
  max_results: 5
  timeout_sec: 10
```

## Notes
- If CONFIGS.yaml is missing, built-in defaults are used.
- API keys live in environment variables, not in this file.
- Use `--verbose off` to reduce output.
- Use `--web-search always` for testing.
- v0.8 defaults web search to AUTO; set `web_search.mode: "off"` if you want pure corpus mode.
