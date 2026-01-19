# Troubleshooting (When Things Get Weird)

# Troubleshooting (When Things Get Weird)

This repo is designed to be low-drama, but your machine did not get that memo. Troubleshooting exists because “it should work” is not a strategy, and because the fastest way to quit a learn-by-building project is to get stuck on the same dumb error for 45 minutes.

This doc is not a novel. It’s a set of quick fixes for common failure modes, written for PMs who want progress, not a surprise masterclass in Python packaging, API keys, or Docker politics.

## Overview

When something breaks, start by classifying the break. Most issues fall into a small set of buckets:

- **Environment/setup**: wrong Python version, missing dependencies, venv not activated
- **API keys**: missing key, wrong key, key not exported in your shell
- **Model/provider**: asking for a model you don’t have access to, wrong provider selected
- **Indexing**: corpus not indexed yet, index path wrong, database missing
- **Web search**: web search enabled but provider not configured, Docker not running, port conflicts
- **Output noise**: too verbose, hard to see the answer, logs drowning the signal

The goal is to get you unstuck fast:
1) identify the bucket
2) apply the fix
3) rerun the exact same command
4) move on with your life

---

## Specific Troubleshooting tips

### Missing API key
- `printenv ANTHROPIC_API_KEY`
- Add to your shell profile and re-source
- if you're on a Mac, don't forget to `source ~/.zshrc` to make the changes active

### Model key mismatch
- GPT models need OPENAI_API_KEY
- Claude models need ANTHROPIC_API_KEY

### Too much output
- Use `--verbose off`

### Docker search issues
- If container is restarting:
  ```
  docker rm -f searxng
  ```
- If connection refused: wait and rerun
- If Docker feels heavy: use API search

### "command not found: python"
- Try `python3`

### Setup fails
- Confirm Python 3.9+
- Try `pip install --upgrade pip`
