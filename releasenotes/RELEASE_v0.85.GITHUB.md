# v0.85 - Dean-i-fried Response Mode

Release date: 2026-01-23

This release adds one focused capability: an optional Dean‑i‑fried response mode
that blends direct + inferred answers into a Dean‑style synthesis.

## Highlights
- `--deanifried on|off` and `--deanifried-platform cli|x|linkedin|reddit|substack`
- `CONFIGS.yaml` support under `output.deanisms.deanifried_response`
- Adds a second LLM call (extra cost + latency)

## How to use
```bash
python explore.py "Why does SAFe suck?" --deanifried on
python explore.py "Why does SAFe suck?" --deanifried on --deanifried-platform substack
```

## Notes
- Quality varies by model; some are bolder than others.
- Platform length targets are best‑effort until v1.35 adds hard checks.
- No changes to attribution, metadata preservation, or the CLI workflow.

## Not included
- Lenny Therapy mode (planned v0.86)
- explore.py diagnostic logs (planned v0.9)
- Jupyter notebooks (v1.0)
- Streamlit UI (v2.0)
- Windows support (v3.0)
