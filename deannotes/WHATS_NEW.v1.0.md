# What's New in v1.0 — Self-Contained Corpus Pipeline

The ChatPRD upstream was a generous gift. But a research tool that depends on someone else's commit schedule isn't really a research tool — it's a waiting room. v1.0 fixes that.

`fetch_corpus.py` pulls Lenny's podcast transcripts directly from YouTube using yt-dlp and youtube-transcript-api. No YouTube API key. No Google Cloud account. No waiting for a PR to merge. New episodes show up when Lenny publishes them, not when an upstream maintainer notices.

Run it in batches. Run it all at once. Run a dry-run first to see exactly what it would fetch before writing a single file. The sync state tracks what's already been fetched so you never double-process an episode.

Keeping the corpus current in an era of disruptive innovation is paramount. This makes freshness a property of the tool, not a prayer.

## What changed

- `fetch_corpus.py` — new corpus pipeline script
- `requirements.txt` — added `youtube-transcript-api`, `yt-dlp`
- `CONFIGS.yaml` — added `pipeline:` section with channel URL and behavior knobs

## How to use it

```bash
source .venv/bin/activate

# See what's new without writing anything
python fetch_corpus.py --dry-run

# Fetch in batches (sync state tracks progress between runs)
python fetch_corpus.py --limit 6
python fetch_corpus.py --limit 6
python fetch_corpus.py             # gets the rest

# Or fetch everything at once
python fetch_corpus.py

# Then re-index
python index_corpus.py
```

## Flags

| Flag | What it does |
|---|---|
| `--dry-run` | Preview what would be fetched, write nothing |
| `--limit N` | Fetch N new episodes this run (safe to run again for the next batch) |
| `--full` | Re-fetch all episodes, ignoring sync state |
| `--no-keywords` | Skip Haiku keyword generation (faster, no API call) |

## Config knobs (CONFIGS.yaml)

```yaml
pipeline:
  channel_url: "https://www.youtube.com/@LennysPodcast"
  auto_index_after_fetch: false   # set true to chain index automatically
  generate_keywords: true         # Haiku keywords per episode (optional)
  max_episodes: null              # null = no limit
```
