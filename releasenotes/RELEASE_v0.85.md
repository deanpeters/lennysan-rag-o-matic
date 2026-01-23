# v0.85 - Dean-i-fried Response Mode 🎭

**Release Date:** January 23, 2026  
**Status:** Mac-only, CLI-only, optional voice layer

v0.85 adds one focused capability: **an optional Dean‑i‑fried response mode** that blends direct + inferred answers into a Dean‑style synthesis.

## What’s New (One Feature)

### ✅ Dean-i-fried (Optional)
- New CLI flags: `--deanifried on|off` and `--deanifried-platform cli|x|linkedin|reddit|substack`
- New config block in `CONFIGS.yaml` under `output.deanisms.deanifried_response`
- Adds a second LLM call to synthesize a Dean‑style response

## How to use

```bash
python explore.py "Why does SAFe suck?" --deanifried on
python explore.py "Why does SAFe suck?" --deanifried on --deanifried-platform substack
```

## Important Notes

- Dean‑i‑fried **adds cost + latency** (extra LLM call).
- Output quality varies by model; Sonnet tends to be bolder than GPT‑4o.
- Platform length targets are **best‑effort** until v1.35 adds hard checks.

## What Didn’t Change

- YAML metadata preservation end‑to‑end
- Source attribution formatting
- Local embeddings + ChromaDB
- Web search fallback behavior

## What This Is NOT (Yet)

- ❌ Lenny Therapy mode (planned v0.86)
- ❌ explore.py diagnostic logs in logs/ (planned v0.9)
- ❌ Jupyter notebooks (v1.0)
- ❌ Streamlit UI (v2.0)
- ❌ Windows support (v3.0)

## Philosophy Reminder

**One feature per version.** v0.85 is Dean‑i‑fried only.
