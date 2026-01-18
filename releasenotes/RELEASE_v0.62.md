# v0.62 - Flexible CLI Args 🧩

**Release Date:** January 18, 2026  
**Status:** Mac-only, CLI-only

v0.62 adds one small UX improvement: **argument order flexibility**.

## What’s New (One Small Improvement)

### ✅ Flexible Argument Order
You can now place the quoted question **before or after** `--model`:

```bash
python explore.py "why does SAFe suck?" --model gpt-4o
python explore.py --model sonnet-4 "What's the fuss about business models?"
```

## What Didn’t Change

- CONFIGS.yaml behavior
- Model switching options
- Retrieval + prompt format

