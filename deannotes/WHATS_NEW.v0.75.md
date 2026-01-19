# What's New in v0.75 (For PMs)

v0.75 adds one new capability: web search fallback.
If the Lenny corpus cannot answer your question, the tool can optionally
search the web and surface those sources alongside the corpus results.

This is still a CLI-first, low-barrier workflow. Nothing changes about
metadata preservation or attribution. The difference is that out-of-scope
questions now have a graceful, explicit fallback path.

## Why it matters
- You can ask broader questions without getting a dead end.
- You get web sources as links, clearly separated from corpus sources.
- You stay in control of cost and quota.

## How to use it

```bash
# Conservative, auto-triggered fallback
python explore.py --web-search on "why safe sucks"

# Force a search every time (useful for testing)
python explore.py --web-search always "why safe sucks"
```

## What stayed the same
- One feature per version
- CLI-first workflow
- YAML metadata preservation
- Attribution in every answer

## What is not included yet
- Docker/SearXNG fallback (planned v0.8)
- explore.py diagnostic logs (planned v0.9)
- Jupyter notebooks (v1.0)

If you are tuning heuristics, use AUTO mode for normal use and ALWAYS
only when you need to verify that web search is working.
