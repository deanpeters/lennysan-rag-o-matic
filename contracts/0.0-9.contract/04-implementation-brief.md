# Implementation Brief (0.x)
04-implementation-brief.md

This document defines exactly what must be implemented for Version 0.x
and how that implementation must behave.

It translates the Constitution and User Journey into concrete,
testable execution rules.

If implementation decisions conflict with this brief,
the implementation is wrong.

---

## Scope of 0.x Implementation

0.x delivers a CLI-first RAG system that:
- preserves metadata end-to-end
- keeps setup low-barrier
- exposes costs and configuration
- supports model switching
- supports optional web search fallback

0.x does not add notebooks, dashboards, or multi-corpus support.

---

## Canonical User Actions

From the repository root, a user can run:

~~~text
./setup.sh
python explore.py "your question here"
~~~

These actions must result in:
- a local index that persists to disk
- an answer with explicit sources
- clear guidance on what was used and what was missing

---

## Metadata Preservation (Non-Negotiable)

Implementation must:
- parse YAML frontmatter separately
- attach metadata to every chunk
- store metadata in the vector database
- retrieve and print metadata in answers

If attribution is weakened, the implementation violates this contract.

---

## Configuration Discipline

All defaults must live in CONFIGS.yaml.

Implementation must:
- read config at runtime
- allow CLI overrides without hiding defaults
- avoid duplicate config files
- use environment variables for secrets only

---

## Model Switching (Required)

Implementation must:
- accept `--model <name>`
- list models via `--list-models`
- map user-friendly names to provider IDs
- present model choice and cost caveats in output

---

## Web Search Fallback (Optional)

Implementation must:
- accept `--web-search on|off|always`
- default to CONFIGS.yaml
- disable search with a warning if API key is missing
- surface when search was engaged
- print web sources distinctly

AUTO fallback must be conservative.
ALWAYS is a forced override for testing.

---

## Verbose Controls

Implementation must:
- accept `--verbose on|off`
- default to CONFIGS.yaml
- reduce noise for non-technical users when off

Diagnostic logs must not store full prompts or API keys; keep logs operational only.

---

## Output Structure (Required)

Responses must use a stable structure:
- Direct answer
- Indirect but relevant insights
- What's missing
- Sources (deduped)

If the structure is removed, PMs lose the teaching benefit.

---

## Definition of Done for 0.x

0.x is complete when:
- setup is one command
- the CLI answer is clear and attributed
- configuration is centralized and visible
- model switching works predictably
- web search is optional and transparent

If the system feels clever but fragile, stop and simplify.

---

End of document
