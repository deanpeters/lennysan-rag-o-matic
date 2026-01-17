# v0.5 - Model Switching 🎛️

**Release Date:** January 17, 2026  
**Status:** Mac-only, CLI-only, Anthropic + OpenAI

v0.5 adds one focused capability: **model switching**. You can now choose between Claude and GPT models from the command line without changing code.

## What’s New (One Feature)

### ✅ Model Switching
- `--model` flag to choose your LLM at query time
- `--list-models` to see available options
- Provider-aware API key checks (Anthropic vs OpenAI)
- Pedagogic response structure: direct + inferred + missing

## Available Models (v0.5)

**Anthropic**
- `haiku` → `claude-haiku-4-5-20251001` (cheapest)
- `sonnet-4` → `claude-sonnet-4-20250514` (balanced)

**OpenAI**
- `gpt-4o-mini` → `gpt-4o-mini` (cheapest OpenAI)
- `gpt-4o` → `gpt-4o` (quality OpenAI)

## How To Use (Pedagogic Quick Start)

```bash
# Activate the environment (required)
source activate.sh

# See the model list
python explore.py --list-models

# Default model (Claude Haiku)
python explore.py "What does Lenny say about pricing?"

# Choose a model explicitly
python explore.py --model sonnet-4 "What does Lenny say about pricing?"
python explore.py --model gpt-4o-mini "What does Lenny say about pricing?"
```

## API Keys (What You Need in ~/.zshrc)

- **Anthropic** (for Claude models):
  ```bash
  export ANTHROPIC_API_KEY='sk-ant-...'
  ```

- **OpenAI** (for GPT models):
  ```bash
  export OPENAI_API_KEY='sk-...'
  ```

If you only use Claude models, you only need the Anthropic key.

## Smoke Tests Run (Cheapest First)

- ✅ `--model haiku` (Anthropic) — succeeded
- ✅ `--model gpt-4o-mini` (OpenAI) — succeeded

## Prompt Tuning Notes (What We Learned)

We had to iterate on the response prompt to keep **OpenAI and Sonnet** from being overly strict.
Early versions returned “no context” too often even when relevant snippets were present.
The final prompt asks for a **best‑effort direct answer grounded in context**, then separates
**inferred insights** and **what’s missing**. This keeps answers useful without hallucinating.

## What Didn’t Change

- YAML metadata preservation end‑to‑end
- Source attribution formatting
- Local embeddings + ChromaDB
- Mac‑only CLI workflow

## What This Is NOT (Yet)

- ❌ CONFIGS.yaml (v0.6)
- ❌ Web search fallback (v0.75)
- ❌ Jupyter notebooks (v1.0)
- ❌ Streamlit UI (v2.0)
- ❌ Windows support (v3.0)

## Philosophy Reminder

**One feature per version.** v0.5 is model switching only. Everything else stays stable.
