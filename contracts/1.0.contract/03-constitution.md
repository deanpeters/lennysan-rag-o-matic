# The Constitution
03-constitution.md

This document is the governing contract for Version 1.0 of this repository.

It defines the non-negotiable principles, boundaries, and behaviors that constrain
how this system is designed, built, used, and evolved.

If any implementation, contribution, or AI-generated output conflicts with this
Constitution, the Constitution takes precedence.

This document exists to protect intent over convenience.

---

## Article 1: Purpose

The primary purpose of this repository is to help Product Managers develop judgment.

It does this by:
- grounding exploration in real evidence
- encouraging slow, reflective thinking
- making tradeoffs visible rather than abstract
- supporting reproducible inquiry

This repository is not optimized for speed of output.
It is optimized for quality of thought.

---

## Article 2: Dual Nature of the System

This system is both:

1. A **pedagogic tool**
2. A **practical research tool**

Pedagogy is the primary concern.
Research utility is a strong secondary concern.

When these two are in tension:
- pedagogy wins
- safety wins
- clarity wins

A system that produces impressive results but teaches poor habits
is considered a failure.

---

## Article 3: Primary User

The primary user is a Product Manager who:

- is capable and thoughtful
- may not be deeply technical
- is cautious about breaking systems
- values explanation over magic

The system must assume:
- curiosity, not incompetence
- intent, not misuse
- learning, not performance optimization

If a user feels anxious, confused, or excluded,
the system has violated this Constitution.

---

## Article 4: The Notebook as the Core Interface

Jupyter notebooks are the primary interface for learning and research.

They are not:
- an implementation detail
- a debugging surface
- a provisioning mechanism

A notebook must:
- explain itself before asking the user to act
- be readable without execution
- run top-to-bottom safely
- remain understandable when reopened weeks later

A notebook that requires tribal knowledge is unconstitutional.

---

## Article 5: One Topic, One Notebook

Each topic has exactly one notebook.

The structure is fixed:

~~~text
notebooks/<topic_slug>/
  <topic_slug>.ipynb
  data/
    <topic_slug>.jsonl
    manifest.json
~~~

This structure exists to:
- reduce cognitive load
- reinforce focus on one question at a time
- enable clean reuse and sharing
- support low-risk pull requests

Multi-topic notebooks, dashboards, or notebook orchestration
are explicitly out of scope for Version 1.0.

---

## Article 6: Self-Contained Topic Kits

Each topic folder is a self-contained learning and research kit.

A topic kit must be:
- understandable in isolation
- movable as a single unit
- shareable via zip or pull request
- runnable without external setup

This design intentionally favors portability over global optimization.

---

## Article 7: Build-Time vs Learn-Time (Foundational)

The system enforces a strict separation between build-time and learn-time.

### Build-Time
- API calls are allowed and expected
- data is generated intentionally
- cost is incurred knowingly
- outputs are written to disk

Build-time is explicit and opt-in.

### Learn-Time
- notebooks read prepared files only
- no API calls occur by default
- no data regeneration occurs
- execution is safe and repeatable

Violating this separation breaks trust and pedagogy
and is therefore unconstitutional.

---

## Article 8: Data Hierarchy

Canonical data lives in:
- episodes/
- index/

Topic data is derived data.

Derived data:
- must not redefine canonical semantics
- must be reproducible
- exists to support inquiry, not authority
- is allowed to be incomplete or biased

Confusing derived data with canonical data
is a design failure.

---

## Article 9: Configuration Discipline

CONFIGS.yaml is the single source of truth for non-secret configuration.

Rules:
- no hardcoded model names or parameters
- no hidden configuration in notebooks
- no parallel config files
- secrets only via environment variables

Configuration exists to make tradeoffs visible,
not to obscure them.

---

## Article 10: Reuse Is the Default

If a topic already exists:
- reuse is recommended
- variation is optional
- duplication is discouraged

This reduces:
- duplicated cost
- fragmented thinking
- parallel reinvention

Reuse is not laziness.
Reuse is respect for prior work.

---

## Article 11: Sharing Is Encouraged, Not Required

Users may contribute:
- topic notebooks
- derived datasets
- improved framing or commentary

Contribution is optional.

Imperfect work is welcome.
Polish is not required.

Fear of contribution indicates a failure of system design.

---

## Article 12: Community Cost Defrayment

This system is designed to distribute cost across a community.

When a topic is shared:
- time spent is amortized
- compute cost is not repeatedly incurred
- future users start further along

This is an intentional economic design choice,
not an accidental side effect.

---

## Article 13: The System Must Coach

The system should:
- explain what is happening
- explain why it matters
- suggest next questions

Silence is a missed teaching opportunity.
Over-automation is a missed learning opportunity.

---

## Article 14: Observability Without Overload

The system must make clear:
- what it is doing
- when it is finished
- where outputs are written

User-facing messages must be plain language.
Technical logs may exist elsewhere.

The user should never feel blind.

---

## Article 15: Narrow Vertical Slices

Work must be delivered in narrow vertical slices.

A valid slice:
- begins with user intent
- ends with visible learning value

Speculative abstraction is prohibited.

---

## Article 16: Delivery Over Perfection

Working systems that support learning
are preferred over perfect systems that delay it.

Clarity beats completeness.
Momentum beats polish.

---

## Article 17: Change Discipline

Breaking changes require:
- explicit acknowledgement
- contract updates first
- clear communication

Code must not silently redefine behavior.

---

## Article 18: Permanent Non-Goals

This system is not:
- a data science platform
- a general-purpose RAG framework
- a notebook orchestration system
- an automation-first product

If it starts to resemble these,
the contract has been violated.

---

## Article 19: What Success Feels Like

Success is when:
- users trust the system
- learning feels calm and focused
- notebooks fade into the background
- thinking moves to the foreground

If users talk more about tooling than insight,
the system has failed.

---

## Article 20: Supremacy Clause

This Constitution supersedes:
- convenience
- cleverness
- tool defaults
- implementation shortcuts

When in doubt:
- choose simplicity
- choose pedagogy
- choose trust

---

End of Constitution
