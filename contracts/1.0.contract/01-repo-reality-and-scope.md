# Repo Reality and Scope
01-repo-reality-and-scope.md

This document establishes the factual reality of the repository at the start of Version 1.0
and defines the scope boundaries for all work governed by this contract.

It exists to prevent accidental rewrites, silent regressions, and scope drift.

This document describes what is true today.
It does not speculate about the future.

---

## Current Repository Reality

At the start of Version 1.0, this repository already contains working systems.

These include:

- CONFIGS.yaml at the repository root
- episodes/ containing the canonical transcript corpus
- index/ containing derived indexing artifacts
- explore.py as a CLI-based exploration tool
- index_corpus.py as the indexing script
- scripts/ containing supporting utilities
- releasenotes/ documenting historical changes

These components are in active use.

They are not experimental.
They are not placeholders.

---

## Canonical Data Sources

The following directories are authoritative:

- episodes/
  The canonical transcript corpus

- index/
  Derived indexing artifacts built from the corpus

All topic-based datasets introduced in Version 1.0 are **derived data**.

Derived data:
- must not replace canonical data
- must not redefine indexing semantics
- must be reproducible from canonical sources
- exists to support learning and research workflows

---

## Configuration Reality

CONFIGS.yaml already exists and is in use.

It is the single source of truth for:
- model selection
- temperature
- token limits
- other non-secret configuration

Secrets are provided via environment variables.

Version 1.0:
- reinforces this model
- does not introduce parallel configuration mechanisms
- does not hide configuration inside notebooks or scripts

---

## Existing Script Behavior

The following scripts exist and must continue to function:

- explore.py
- index_corpus.py

Version 1.0 must not:
- rename these scripts
- change their primary behavior
- introduce breaking changes without explicit versioning

New scripts may be added, but only additively.

---

## What Version 1.0 Is Adding

Version 1.0 introduces a **new learning and research interface**.

Specifically:
- topic-based notebooks
- self-contained topic kits
- explicit build-time data generation
- governed notebook behavior

These additions are:
- additive
- opt-in
- non-disruptive to existing workflows

CLI-based exploration remains valid and supported.

---

## What Version 1.0 Is Not Doing

Version 1.0 does not:

- replace the existing CLI tools
- redesign the indexing pipeline
- restructure the transcript corpus
- consolidate exploration paths
- introduce orchestration frameworks
- require notebooks for all use cases

Notebooks are a supported interface, not a mandate.

---

## Scope Boundaries (Explicit)

Version 1.0 work is in scope if it:

- supports the defined user journey
- reinforces pedagogic safety
- enables real research without fragility
- preserves existing functionality
- reduces accidental complexity

Work is out of scope if it:

- introduces hidden coupling
- duplicates configuration
- assumes deep technical expertise
- optimizes for cleverness over clarity
- weakens trust in the system

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

## Summary

Version 1.0 is grounded in reality.

It:
- respects what already works
- adds new capability without disruption
- draws clear boundaries
- enforces intentional evolution

Any work that ignores this reality is non-compliant with the contract.

---

End of document
