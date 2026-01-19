# 0.0-0.75 README contract
README.md

This directory defines the contractual and constitutional governance
for Version 0.x (v0.1 through v0.75).

It exists to be read before building, coding, or prompting AI tools.

If you start writing code without reading this directory,
you are explicitly choosing hope over intent.

---

## What this directory is

This directory is a pre-build contract for the 0.x era.

It defines:
- what is being built
- who it is for
- how it is allowed to behave
- how it may evolve
- how humans and AI tools must work together

This is not documentation of the current codebase.
It is a declaration of intent and constraints for a stable 0.x release line.

---

## Why this exists

The 0.x era moved quickly:
- CLI first
- local RAG pipeline
- model switching
- web search fallback
- CONFIGS.yaml governance

Speed is useful, but speed without guardrails creates chaos.
This contract exists to prevent drift, regressions, and hidden cost.

---

## Who this is for

This contract is written for:
- Product Managers building with AI assistance
- Engineers who want clarity before implementation
- Contributors who want intent, not just mechanics
- AI coding tools such as Codex or Claude Code

If you are teaching others how to work with AI tools, this directory is part of the lesson.

---

## How to use this directory (human)

If you are a human about to build or modify this repository:

1. Read this README to understand the purpose of the contract
2. Read the release notes to understand what "0.x" means
3. Read the Constitution to understand the governing principles
4. Use the remaining documents to guide concrete decisions

If you disagree with something here, change the contract first.
Do not "work around" it in code.

---

## How to use this directory (AI tools)

If you are using Codex, Claude Code, or similar tools:

- Point the tool at this directory
- Require it to read all documents before generating code
- Treat these documents as binding constraints
- Reject output that violates them

This directory exists so you do not have to rely on prompting tricks or repeated corrections.

---

## What this contract governs

This contract governs:
- CLI user experience
- data lifecycle and metadata preservation
- configuration discipline
- model switching behavior
- web search fallback rules
- cost and risk exposure
- contribution patterns

It intentionally does not govern:
- notebook design (planned for 1.0)
- UI frameworks
- agentic workflows
- long-term analytics pipelines

Those are deferred to later contracts.

---

## What "0.x" means here

Version 0.x means:
- a stable, teachable CLI path
- a trustworthy local RAG stack
- explicit guardrails for cost, attribution, and configuration
- one feature per release

0.x does not mean "prototype with no rules."
It means "small scope, high clarity."

---

## Files in this directory

- README.md
  How to use this contract before building

- RELEASE_NOTES.md
  What success looks like for v0.1-v0.75

- INSTRUCTIONS_FOR_CODEX.md
  Machine-readable operating rules for AI coding tools

- 00-consistency-check.md
  Verification that the contract documents agree

- 01-repo-reality-and-scope.md
  What exists today and must not be broken

- 02-user-journey.md
  The intended Product Manager CLI experience

- 03-constitution.md
  The governing principles of the system

- 04-implementation-brief.md
  Concrete instructions for what to build in 0.x

- 05-user-experience-pack.md
  Canonical CLI experience guidelines

Read them in order.
They are designed to reduce ambiguity.

---

## Supporting artifacts (historical evidence)

These files capture real 0.x sessions and lessons learned:

- deannotes/SESSION_LOG_PROMPT.md
- deannotes/SESSION.0.1.STORY.md
- deannotes/bash-history.17Jan25-1030aet.log
- deannotes/SESSION.0.5.STORY.md
- deannotes/SESSION.0.5.LOG.md
- deannotes/SESSION.0.6.LOG.md
- deannotes/SESSION.0.75.LOG.md

Use them as context, not as governance.

---

## A final note on discipline

If you find yourself saying:
- "we can clean this up later"
- "the tool will figure it out"
- "this is just temporary"

Stop.

Those are signals that the contract needs revision.

Change the contract first.
Then build.

---

End of document
