# Product Constitution (v1.0)
CONSTITUTION.md

This document defines the governing principles, constraints, and intent
for this product or system.

It must be written and agreed upon **before** significant implementation begins.

If code, prompts, or AI-generated output conflict with this document,
the Constitution takes precedence.

---

## Article 1: Purpose

The primary purpose of this product is:

> {{STATE THE CORE PURPOSE IN ONE OR TWO SENTENCES}}

This product exists to:
- {{PRIMARY OUTCOME}}
- {{SECONDARY OUTCOME}}

It does **not** exist to:
- {{EXPLICIT NON-GOAL}}
- {{EXPLICIT NON-GOAL}}

Clarity of purpose is more important than feature breadth.

---

## Article 2: Primary User

The primary user is:

> {{DESCRIBE THE USER IN PLAIN LANGUAGE}}

Assumptions about this user:
- {{WHAT THEY CARE ABOUT}}
- {{WHAT THEY FEAR OR AVOID}}
- {{WHAT THEY ARE NOT EXPERT IN}}

The system must optimize for this user first.
Secondary users must not degrade the primary experience.

---

## Article 3: Success Definition

This product is successful when:

- {{USER-OBSERVABLE SUCCESS CRITERIA}}
- {{BEHAVIORAL SIGNAL OF SUCCESS}}
- {{EMOTIONAL SIGNAL OF SUCCESS}}

If success is defined only by metrics and not by user experience,
this Constitution is incomplete.

---

## Article 4: Teaching Posture (If Applicable)

This system:
- does / does not teach users as they interact with it

If teaching is in scope:
- explain before executing
- prefer clarity over cleverness
- surface tradeoffs, not just answers

If teaching is not in scope:
- state that explicitly here

---

## Article 5: Core Interface(s)

The primary interface(s) for this product are:

- {{INTERFACE 1}}
- {{INTERFACE 2}}

These interfaces are:
- intentional
- stable
- designed for the primary user

Anything outside these interfaces is secondary.

---

## Article 6: Safety and Trust Boundaries

The system must:
- {{SAFETY GUARANTEE}}
- {{TRUST GUARANTEE}}

The system must not:
- {{TRUST VIOLATION}}
- {{SURPRISE BEHAVIOR}}

If a user feels anxious, confused, or tricked,
the system has violated this Constitution.

---

## Article 7: Cost and Risk Discipline

Costs and risks must be:
- explicit
- opt-in
- visible to the user

The system must not:
- incur cost implicitly
- hide expensive operations
- surprise users with irreversible actions

---

## Article 8: Data and State Principles

Define what is:
- canonical data
- derived data
- temporary state

Rules:
- {{RULE ABOUT MUTATION}}
- {{RULE ABOUT REPRODUCIBILITY}}

Confusing these layers is prohibited.

---

## Article 9: Configuration and Control

Configuration must be:
- centralized
- visible
- auditable

The system must not:
- hide configuration in multiple places
- rely on magic defaults
- require tribal knowledge

---

## Article 10: Reuse and Extensibility

The system should:
- encourage reuse
- allow extension without forking
- avoid unnecessary duplication

Reuse is preferred over reinvention.

---

## Article 11: Community and Contribution (If Applicable)

Contribution is:
- optional / encouraged / required (choose one)

Rules for contribution:
- {{QUALITY BAR}}
- {{EXPECTATIONS}}
- {{WHAT IS WELCOME}}

Fear of contributing indicates poor system design.

---

## Article 12: Scope Boundaries

This product explicitly does **not** aim to be:

- {{NON-GOAL CATEGORY}}
- {{NON-GOAL CATEGORY}}

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
