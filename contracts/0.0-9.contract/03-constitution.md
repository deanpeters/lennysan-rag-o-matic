# Product Constitution (v0.1-v0.75)

This document captures the governing principles, constraints, and intent of the product
as it evolved from v0.1 through v0.75. It is a historical and current governance snapshot.

If code, prompts, or AI-generated output conflict with this document, the Constitution takes precedence.

---

## Article 1: Purpose

The primary purpose of this product is:

> A low-barrier, learn-by-building PM research tool that lets product managers explore Lenny Rachitsky's podcast corpus using RAG.

This product exists to:
- help PMs query and learn from the Lenny corpus with clear attribution
- teach less-technical PMs how to work with repos, CLI tools, and AI safely

It does not exist to:
- be a general web-research platform or chatbot without citations
- replace dedicated BI/analytics or fully-fledged knowledge management systems

Clarity of purpose is more important than feature breadth.

---

## Article 2: Primary User

The primary user is:

> A product manager who is comfortable with basic CLI use but not a professional programmer.

Assumptions about this user:
- cares about clarity, attribution, and credibility
- fears hidden costs, brittle setup, and confusing error messages
- is not expert in Python packaging or infra

The system must optimize for this user first.
Secondary users must not degrade the primary experience.

---

## Article 3: Success Definition

This product is successful when:
- a PM can run setup and query the corpus with minimal friction
- answers include clear, reliable source attribution (guest/title/date/URL)
- users feel confident and learn how the system works

If success is defined only by metrics and not by user experience,
this Constitution is incomplete.

---

## Article 4: Teaching Posture

This system does teach users as they interact with it.

Teaching guidelines:
- explain before executing
- prefer clarity over cleverness
- surface tradeoffs, not just answers

---

## Article 5: Core Interface(s)

Primary interfaces:
- CLI (explore.py)
- One-command setup (setup.sh)
- Configuration (CONFIGS.yaml)

These interfaces are:
- intentional
- stable
- designed for the primary user

Anything outside these interfaces is secondary.

---

## Article 6: Safety and Trust Boundaries

The system must:
- preserve YAML metadata end-to-end
- always show attribution for top sources
- warn when web search is requested but API key is missing

The system must not:
- weaken or remove citations
- imply it used the web when it did not

If a user feels anxious, confused, or tricked,
the system has violated this Constitution.

---

## Article 7: Cost and Risk Discipline

Costs and risks must be:
- explicit
- opt-in
- visible to the user

The system must not:
- incur web/API costs silently
- hide expensive operations
- surprise users with irreversible actions

---

## Article 8: Data and State Principles

Canonical data:
- episodes/**/transcript.md (YAML frontmatter + transcript content)

Derived data:
- data/chroma_db/ (vector database)

Temporary state:
- .venv/, logs/

Rules:
- do not mutate source transcripts
- derived artifacts must be reproducible

Confusing these layers is prohibited.

---

## Article 9: Configuration and Control

Configuration must be:
- centralized
- visible
- auditable

The system must not:
- hide config across multiple files
- rely on magic defaults
- require tribal knowledge

CONFIGS.yaml is the canonical default source of truth;
CLI flags may override but should not hide defaults.

---

## Article 10: Reuse and Extensibility

The system should:
- encourage reuse
- allow extension without forking
- avoid unnecessary duplication

Reuse is preferred over reinvention.

---

## Article 11: Community and Contribution

Contribution is: encouraged

Rules for contribution:
- preserve attribution and metadata rules
- keep one-feature-per-version discipline
- update docs before tagging releases

Fear of contributing indicates poor system design.

---

## Article 12: Scope Boundaries

This product explicitly does not aim to be:
- a general web-research engine
- a full notebook platform (until v1.0)

If the system starts resembling these,
the Constitution must be revisited.

---

## Article 13: Delivery Philosophy

The system prioritizes:
- working over perfect
- clarity over completeness
- narrow slices over broad ambition

Speculative abstraction is discouraged.

---

## Article 14: Change Discipline

Breaking changes require:
- explicit acknowledgement
- documentation updates first
- user-visible communication

Code must not silently redefine behavior.

---

## Article 15: Supremacy Clause

This Constitution supersedes:
- tooling defaults
- AI suggestions
- implementation convenience
- time pressure

When in doubt:
- choose simplicity
- choose trust
- choose the user

---

End of Constitution
