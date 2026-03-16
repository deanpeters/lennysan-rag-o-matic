# Lenny Therapy Mode — Vision & Approach

## Pre-code checklist (do this before we write a line of code)

- Decide: **new entry point** (`therapy.py`) vs `explore.py --mode therapy` (recommend `therapy.py`).
- Confirm **output structure invariant** (reflection → reframe → evidence → open question).
- Define **tone boundaries** (no clinical/therapy claims, no prescriptions, no authority voice).
- Decide whether **web search** stays allowed in therapy mode (recommended: yes, optional).
- Decide **model defaults** for therapy mode (Haiku vs Sonnet vs GPT‑4o).
- Confirm whether we are **skipping the Golden dataset** in v0.86 (recommended: skip, prompt‑only).

## Vision

Lenny Therapy Mode is an **optional facilitation layer** on top of LennySan RAG-o-Matic that helps product managers think more clearly in moments of stress, ambiguity, or frustration — without turning the system into a therapist, coach, or advice engine.

The core idea is simple:
**the “group” is the collective experience of every guest who has ever been on Lenny’s Podcast, and Lenny’s role is the facilitator, not the authority.**

Instead of only returning answers, frameworks, or tactics, this mode reframes retrieved insights into **thought-provoking facilitator questions** that help users reflect, re-interpret, and regain agency around everyday product-management anxieties (executive overrides, roadmap churn, misalignment, burnout, uncertainty).

This is not mental health care.
It is **facilitated professional reflection**, grounded in real evidence from the corpus.

---

## What Changes in Lenny Therapy Mode

When enabled, the system still does everything it does today:

- Retrieve **direct evidence** from transcripts
- Surface **inferred insights** (clearly labeled)
- Optionally incorporate **web search** when the corpus is thin

But instead of ending with “here’s the answer,” the system **shapes its output through a facilitator lens**:

- Reflecting emotions without diagnosing them
- Normalizing common PM struggles using group voices
- Reframing unhelpful interpretations into clearer questions
- Encouraging small, concrete thinking steps instead of prescriptions

The output shifts from *instruction* to *facilitation*.

---

## The Facilitation Techniques (Non-Clinical, Explicitly Scoped)

Lenny Therapy Mode draws inspiration from well-known **group facilitation and reflection techniques**, applied in a **non-clinical, professional context**, including:

- Normalization and validation (naming feelings, showing they’re common)
- Perspective-shift questions (“another way to look at this might be…”)
- Cognitive reframing (challenging stuck interpretations, not emotions)
- Values and priorities exploration (what actually matters here)
- Behavioral experiment framing (small, low-risk next steps)
- Group-reflection prompts (what others felt, tried, and learned)

These techniques are used **only to shape questions and reflections**, not to diagnose, treat, or advise.

---

## Governance First: Contracts and Constitutions

This mode is introduced **only after governance is explicit**.

Before any facilitation behavior is added, the project establishes:

- **`contract.md`** — what Lenny Therapy Mode is designed to do, and what it explicitly does not do
- **`constitution.md`** — how the system is allowed to behave: tone, boundaries, prohibitions, and escalation limits

This makes the mode:
- Tool-agnostic (works across Claude Code, Codex, future agents)
- Explainable to humans
- Safer to extend without accidental scope creep

If code and governance disagree, **governance wins**.

---

## Facilitation First Principle

When users express frustration, anxiety, or emotional load, the system must respond with **reflection and reframing before introducing evidence, frameworks, or tactics**.

Evidence supports facilitation — it does not replace it.
This ordering is intentional and non-negotiable in Lenny Therapy Mode.

---

## Output Shape Invariant

In Lenny Therapy Mode, responses should typically follow this structure:

1. Reflection and normalization (naming what’s being felt or experienced)
2. Reframed perspective or facilitator-style question
3. Optional grounded evidence (direct + inferred, clearly labeled)
4. An open-ended facilitator question — never a prescription

This invariant exists to keep the system grounded, calm, and user-directed.

---

## How It Works Under the Hood (High Level)

1. **Evidence retrieval**
   - Pull transcript chunks (the “group voices”) with citations
   - Optionally supplement with web search

2. **Facilitation shaping**
   - Select facilitator question patterns informed by known techniques
   - Reframe evidence into reflective, open-ended prompts

3. **Structured output**
   - Direct insights (grounded)
   - Inferred insights (clearly labeled)
   - Missing information (explicit)
   - Facilitator question to guide the next turn

The system never invents authority; it **orchestrates voices and questions**.

---

## Implementation Approach (CLI First, No Duplicate Code)

Lenny Therapy Mode will likely ship as a **separate Python entry point** (for example, `therapy.py`) that runs similarly to `explore.py`, but produces facilitator-shaped output.

To avoid duplicate logic, shared behavior will be factored into a small internal library that both scripts can import, such as:

- configuration loading and validation
- model/provider selection
- retrieval and citation formatting
- “direct vs inferred vs missing” response scaffolding
- optional web search fallback

The refactor should be **planned before executed**, using Claude Code or Codex to propose a minimal, low-risk structure that preserves the repo’s learn-by-building nature.

---

## Golden Data Strategy: Building a Facilitator Question Library

To make facilitation behavior consistent and explainable, the project will build a **Golden dataset** of facilitator question patterns.

This dataset may be bootstrapped from **open-source collections of group reflection questions**, then adapted into a Lenny-style facilitation voice.

### Likely construction process

- Identify permissively licensed, open-source datasets of group reflection or facilitation questions
- Use lightweight CLI tooling (`grep`, `awk`, `sed`) to extract all questions Lenny asks from transcripts into a raw text dataset
- Categorize questions by function and consolidate near-duplicates into exemplar forms
- Use generative AI to reframe open-source question patterns into Lenny’s facilitator voice, grounded in the extracted Lenny-question dataset

The result is an inspectable, versioned artifact that shows how raw facilitation prompts become **Lenny-style facilitator questions**.

---

## Explicit Non-Goals

Lenny Therapy Mode will not:

- Diagnose, treat, or provide mental health care
- Act as a coach, manager, or executive proxy
- Escalate emotional intensity or simulate clinical therapy
- Replace human judgment or decision-making

This mode exists to support thinking, not to direct outcomes.

---

## Evolution Over Time

The initial implementation may use only one or two facilitation techniques.
Additional techniques, datasets, and refinements are expected to be layered in incrementally as the Golden dataset matures.

Incomplete by design. Extensible by intent.

---

## Why This Matters

Most AI tools optimize for answers.
Product managers often need **better questions first**.

Lenny Therapy Mode helps slow the moment down, surface collective wisdom, and restore clarity — using the same evidence, shaped through a facilitator’s lens.

Optional. Explicit. Grounded. Explainable.
