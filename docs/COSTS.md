# Costs (What This Actually Costs)

Let’s talk about the thing that turns “fun weekend repo” into “why is Finance emailing me.” This tool is meant to be cheap, but cheap is a choice: model, retrieval size, and web search decide whether you’re spending pennies or lighting a small pile of dollars on fire.

## Overview

This repo costs money in exactly one way: **LLM calls**. Everything else is local.

The cost knobs are simple:
- **Model**: bigger brain, bigger bill
- **Retrieved text**: more chunks = more tokens
- **Web search**: useful, but can increase spend fast
- **Iteration**: ten “quick tries” adds up

Use this mental model:
- **Smoke test**: cheapest model, fewer chunks, quick feedback
- **Deep run**: better model, enough chunks, citations you trust

Set sane defaults in `docs/CONFIGURATION.md`, then upgrade runs on purpose.


---

Baseline numbers (Haiku):
- Setup: $0 (local embeddings)
- Per query: around $0.001 to $0.005
- Local storage: about 500MB

Rule of thumb:
- Haiku / GPT-4o mini for cheap smoke tests
- Sonnet 4 / GPT-4o for deeper runs

This is cheaper than $20/month subscriptions if you only run occasional queries.
