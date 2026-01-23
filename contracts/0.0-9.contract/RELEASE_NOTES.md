# Release Notes - Contract v0.1-v0.75
RELEASE_NOTES.md

These notes define what "done" means for the 0.x era.
They are a future-facing contract grounded in what we learned while shipping v0.1 through v0.75.

This is a contract for intent and behavior, not a changelog of commits.

---

## What 0.x Represents

Version 0.x is a commitment to:
- a low-barrier CLI experience
- trustworthy attribution and metadata preservation
- explicit cost and configuration discipline
- one feature per release

It is not a promise of UI polish, notebook workflows, or automation frameworks.

---

## What "Shipped" in 0.x (Contractually)

### 1) A Teachable CLI RAG Path
The primary interface is the CLI:
- `setup.sh` for setup and indexing
- `explore.py` for queries

This is intentional and governed.

### 2) Metadata Preservation End-to-End
All retrieval and output flows preserve YAML frontmatter:
- guest
- title
- date
- URL

This is non-negotiable and a trust anchor.

### 3) Model Switching (v0.5)
Users can switch LLMs with a `--model` flag.
Models are declared in CONFIGS.yaml and can be listed via `--list-models`.

### 4) CONFIGS.yaml Governance (v0.6)
CONFIGS.yaml is the single source of truth for:
- model defaults
- retrieval parameters
- CLI defaults
- web search settings

Configuration is visible and auditable.

### 5) Web Search Fallback (v0.75)
Web search is optional and controlled:
- AUTO: only when direct answer confidence is weak
- ALWAYS: force web search (useful for testing)
- OFF: never search

If API key is missing, search is disabled with a clear warning.

### 6) Verbose Controls
CLI output is controllable via `--verbose on|off`.
Default verbosity is defined in CONFIGS.yaml.

---

## What Did Not Ship in 0.x

0.x explicitly excludes:
- notebooks as a primary interface
- multi-corpus support
- web search beyond a simple fallback
- automated topic systems
- rich UIs or dashboards

These are reserved for later contracts.

---

## Next Up in 0.x (Planned)

- v0.8: optional Docker/SearXNG search backend
- v0.85: optional Dean-i-fried response mode (direct + inferred blend)
- v0.86: Lenny Therapy mode (facilitated reflection)
- v0.9: explore.py diagnostic logs in logs/ (system messages, errors)

These are still within the 0.x contract scope and must follow
one-feature-per-version discipline.

---

## Lessons Learned (Now Codified)

- Prompt tweaks can regress behavior; keep overrides and test with multiple models.
- "AUTO vs ALWAYS" matters for both cost control and manual testing.
- Clear, repetitive attribution is better than clever brevity.
- Defaults must live in CONFIGS.yaml and be visible to users.
- Pedagogic clarity is a feature, not a nicety.

---

## Success Criteria for 0.x

0.x is successful if:
- a PM can set up and query with minimal friction
- answers include trustworthy sources
- cost exposure is visible and opt-in
- prompts and outputs teach as they inform

If the system feels fast but fragile, the contract has failed.

---

## Known and Intentional Limitations

- Web search is a fallback, not a research engine
- Heuristics are conservative to protect quota
- CLI-first limits discovery for non-terminal users

These limitations are accepted to protect clarity and trust.

---

End of document
