# Repo Reality and Scope (0.x)
01-repo-reality-and-scope.md

This document establishes the factual reality of the repository in the 0.x era
and defines the scope boundaries for all work governed by this contract.

It exists to prevent accidental rewrites, silent regressions, and scope drift.

This document describes what is true today.
It does not speculate beyond the 0.x contract.

---

## Current Repository Reality (0.x)

At the end of v0.75, this repository already contains working systems.

These include:
- CONFIGS.yaml at the repository root
- episodes/ containing the canonical transcript corpus
- data/chroma_db/ as derived vector storage
- explore.py as a CLI-based exploration tool
- index_corpus.py as the indexing script
- setup.sh as the one-command bootstrap
- releasenotes/ documenting historical changes

These components are in active use.
They are not experimental.
They are not placeholders.

---

## Historical Learning Artifacts

The repository includes session logs and story notes in deannotes/.
These are not contracts, but they inform why 0.x governance exists.

---

## Canonical Data Sources

The following directories are authoritative:
- episodes/ (canonical transcript corpus)

Derived data:
- data/chroma_db/ (vector database)

Rules:
- do not mutate the source transcripts
- derived artifacts must be reproducible
- metadata must be preserved end-to-end

---

## Configuration Reality

CONFIGS.yaml already exists and is in use.

It is the single source of truth for:
- model selection defaults
- temperature and token limits
- retrieval parameters
- CLI default flags (verbose, web-search)
- web search provider settings

Secrets are provided via environment variables only.
No parallel config files are allowed.

---

## Existing Script Behavior

The following scripts exist and must continue to function:
- explore.py
- index_corpus.py
- setup.sh

0.x must not:
- rename these scripts
- change their primary behavior
- introduce breaking changes without explicit versioning

New scripts may be added, but only additively.

---

## Web Search Reality (v0.75)

Web search exists as a fallback mechanism:
- AUTO: used only when direct answer is weak
- ALWAYS: forced for testing
- OFF: disabled

If API key is missing, search is disabled with a warning.
This behavior is contractual.

---

## Upstream Corpus Reality

The transcript corpus originates from the upstream repo.
Changes to upstream live outside this repo and are managed via a fork
and pull requests.

This repo should not attempt to mutate upstream data directly.

---

## What 0.x Is Not Doing

Version 0.x does not:
- introduce notebooks as a primary interface
- replace the CLI tools
- redesign the indexing pipeline
- add multi-corpus support
- add orchestration frameworks

Notebooks and expanded UX are reserved for 1.0.

---

## Scope Boundaries (Explicit)

Work is in scope if it:
- supports the CLI user journey
- preserves metadata and attribution
- keeps configuration centralized
- teaches as it informs
- reduces accidental complexity

Work is out of scope if it:
- introduces hidden coupling
- duplicates configuration
- assumes deep technical expertise
- weakens trust in outputs

---

## Change Discipline

If a proposed change:
- breaks an existing workflow
- alters canonical data semantics
- changes configuration behavior
- expands scope materially

The contract must be updated first.

Code must not lead governance.

---

End of document
