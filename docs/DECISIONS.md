# Decision Log (Big Moves Only)

## Overview

This is the running log of major product and architecture decisions. If a change alters behavior, cost, or user trust, it belongs here, with the “why” written down so future you doesn’t have to play detective.

This is not a diary. It’s the short list of “we bet the repo on this” decisions that keep the system coherent as it grows. If you’re proposing a meaningful change, you should be able to point to an existing decision here or add a new one.

**Sources for decisions** live in the session history:
- [deannotes/](deannotes/) (session logs folder, including `SESSION.*.LOG.md`)
- [deannotes/SESSION.0.1.STORY.md](deannotes/SESSION.0.1.STORY.md)
- [deannotes/SESSION_LOG_PROMPT.md](deannotes/SESSION_LOG_PROMPT.md)

Only log decisions that change the shape of the product, like:
- defaults and configuration philosophy
- cost-control rules
- citation and traceability requirements
- web search policy and provider tradeoffs
- logging, privacy, and “what we store” boundaries

Use this doc when you want to:
- understand the repo’s non-negotiables
- justify a design choice to a skeptical PM or engineer
- change behavior without accidentally breaking the project’s spine

---

## D001 - Preserve YAML metadata end-to-end
Status: accepted
Why: Attribution is foundational to trust and learning.
Impact: parse YAML frontmatter, attach metadata to every chunk, store in ChromaDB,
return sources with guest/title/date/URL.

## D002 - One feature per version
Status: accepted
Why: Keeps scope tight, teaches discipline, makes changes reviewable.
Impact: every release has exactly one major capability.

## D003 - CONFIGS.yaml as single source of truth
Status: accepted
Why: Visible, auditable defaults for non-technical PMs.
Impact: all defaults live in CONFIGS.yaml; CLI flags override but do not hide.

## D004 - Model switching via --model
Status: accepted
Why: Cheap smoke tests vs higher-quality runs.
Impact: --list-models, clear labeling, provider-aware API keys.

## D005 - Web search fallback (AUTO vs ALWAYS)
Status: accepted
Why: Avoid unnecessary cost while still handling out-of-scope queries.
Impact: AUTO is conservative; ALWAYS forces search for testing.

## D006 - Web search must be explicit about cost and keys
Status: accepted
Why: No surprise spend. Keys are user responsibility.
Impact: missing keys disable search with a warning.

## D007 - Docker search is advanced and optional
Status: accepted
Why: Docker adds friction; PMs need a safe default path.
Impact: Docker is opt-in; API remains the default.

## D008 - One-button Docker search (no CONFIG edits)
Status: accepted
Why: Reduce setup friction for PMs who still want OSS search.
Impact: scripts/docker_search.sh starts container and runs explore.py.

## D009 - Diagnostic logs must not store prompts or secrets
Status: accepted
Why: Privacy + cost control.
Impact: logs are operational only (system messages, errors).

## D010 - Do not auto-start Docker
Status: accepted
Why: Surprising behavior, OS-specific, breaks trust.
Impact: warnings + copy-paste instructions instead.

## D011 - Use runtime SearXNG settings
Status: accepted
Why: SearXNG requires a secret key and writes to settings.
Impact: generate logs/searxng.settings.yml and mount read-write.

---

To add a decision:
- append a new D### entry
- explain why and user impact
- link to the session log if helpful
