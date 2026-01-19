# 1.0 README contract
README.md

This directory defines the contractual and constitutional governance for this repository.

It exists to be read **before** building, coding, or prompting AI tools.

If you start writing code without reading this directory, you are explicitly choosing hope over intent.

---

## What this directory is

This directory is a **pre-build contract**.

It defines:
- what is being built
- who it is for
- how it is allowed to behave
- how it may evolve
- how humans and AI tools must work together

This is not documentation of the current codebase.
It is a declaration of intent and constraints for a major release.

---

## Why this exists

Modern development tools make it easy to:
- generate large amounts of code quickly
- explore ideas without friction
- “vibe code” toward something that feels right

They also make it easy to:
- drift into unnecessary complexity
- let tools make architectural decisions
- mistake speed for clarity
- use hope as a strategy

This contract exists to prevent that.

---

## Who this is for

This contract is written for:

- Product Managers designing systems with AI assistance
- Engineers who want clarity before implementation
- Contributors who want to understand intent, not just mechanics
- AI coding tools such as Codex or Claude Code

If you are teaching others how to work with AI tools, this directory is part of the lesson.

---

## How to use this directory (human)

If you are a human about to build or modify this repository:

1. Read this README to understand the purpose of the contract
2. Read the release notes to understand what “1.0” means
3. Read the Constitution to understand the governing principles
4. Use the remaining documents to guide concrete decisions

If you disagree with something here, change the contract first.
Do not “work around” it in code.

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

- user experience
- data lifecycle
- notebook behavior
- configuration discipline
- contribution patterns
- cost and risk exposure
- what is explicitly out of scope

It intentionally does not govern:
- implementation language details
- specific model choices over time
- prompt phrasing experiments
- visual polish

Those are allowed to evolve within the contract.

---

## What “1.0” means here

Version 1.0 does not mean “finished.”

It means:
- the learning interface is intentional
- the structure is stable enough to teach from
- the rules are explicit
- breaking changes are conscious, not accidental

This is a commitment to clarity, not rigidity.

---

## Files in this directory

This directory contains:

- README.md
  How to use this contract before building

- RELEASE_NOTES.md
  What success looks like for version 1.0

- INSTRUCTIONS_FOR_CODEX.md
  Machine-readable operating rules for AI coding tools

- 00-consistency-check.md
  Verification that the contract documents agree

- 01-repo-reality-and-scope.md
  What exists today and must not be broken

- 02-user-journey.md
  The intended Product Manager experience

- 03-constitution.md
  The governing principles of the system

- 04-implementation-brief.md
  Concrete instructions for what to build

- 05-user-experience-pack.md
  The canonical notebook experience

Read them in order.
They are designed to reduce ambiguity.

---

## A final note on discipline

If you find yourself saying:
- “we can clean this up later”
- “the tool will figure it out”
- “this is just temporary”

Stop.

Those are signals that the contract needs revision.

Change the contract first.
Then build.

---

End of document
