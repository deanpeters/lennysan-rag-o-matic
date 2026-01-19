# Notebook UX Pack
05-user-experience-pack.md

This document defines the canonical notebook experience for Version 1.0.

It exists to ensure that every notebook:
- feels safe to open
- teaches while it informs
- reduces intimidation
- reinforces good learning habits

If a notebook violates this UX, it violates the contract.

---

## Purpose of the Notebook UX

Notebooks are the primary interface users will touch.

For many Product Managers, this may be:
- their first sustained interaction with notebooks
- their first time running code-based research artifacts
- their first exposure to RAG-style exploration

The notebook experience must therefore:
- coach, not test
- guide, not impress
- reassure, not surprise

---

## The Notebook Is a Workbook

Every notebook must be treated as a **guided workbook**, not a script dump.

A user should be able to:
- read the notebook without running it
- understand what each section is for
- decide how deeply they want to engage

Execution is optional.
Understanding is mandatory.

---

## Canonical Notebook Structure

Each topic notebook must follow this structure, in order:

1. Orientation and Safety
2. What This Topic Is About
3. What Data This Notebook Uses
4. How to Use This Notebook
5. Guided Exploration Sections
6. Reflection and Next Questions

No sections may be skipped.
Additional sections may be added only if they do not disrupt flow.

---

## Section 1: Orientation and Safety (First Cell)

The first cell must be **Markdown** and must reassure the user.

It must explicitly state:
- what this notebook is
- what it is not
- that it is safe to run
- that no API calls will occur during normal execution

Example (illustrative only):

~~~markdown
# Welcome

This notebook helps you explore the topic: **Why SAFe Sucks**

You do not need Python experience to use this notebook.

You can safely:
- read this notebook without running anything
- run all cells from top to bottom
- rerun cells as many times as you like

This notebook does **not**:
- make API calls
- regenerate data
- modify any files

Nothing will break if you explore.
~~~

This reassurance is non-negotiable.

---

## Section 2: What This Topic Is About

This section frames the question being explored.

It must:
- describe the topic in plain language
- explain why the topic matters
- acknowledge that reasonable people may disagree

It must not:
- assert conclusions
- position the notebook as authoritative
- oversimplify complex tradeoffs

This section sets intellectual tone.

---

## Section 3: What Data This Notebook Uses

This section explains provenance.

It must:
- explain that the data is derived
- explain where it came from conceptually
- mention that it reflects selection and framing choices

It should:
- reference the manifest.json
- encourage healthy skepticism

The goal is trust through transparency.

---

## Section 4: How to Use This Notebook

This section teaches notebook mechanics implicitly.

It must explain:
- how cells work
- that running cells is optional
- that rerunning cells is normal
- that outputs appear below cells

It must assume:
- no prior notebook experience

It must avoid:
- jargon
- shortcuts
- instructions that feel like a test

This is a teaching moment.

---

## Section 5: Guided Exploration

This is the core of the notebook.

Guided exploration sections must:
- introduce a question
- show relevant excerpts or summaries
- provide light structure for thinking
- avoid overwhelming volume

Each subsection should:
- explain why the view exists
- show evidence
- invite interpretation

The notebook should ask:
- “What do you notice?”
- “What surprises you?”
- “What tensions do you see?”

It should not rush to answers.

---

## Section 6: Reflection and Next Questions

Every notebook must end with reflection.

This section should:
- summarize what was explored
- suggest follow-up questions
- encourage reuse or variation
- normalize disagreement

It should explicitly state:
- this notebook is a starting point
- not a final answer

---

## Code Cells: Behavioral Rules

Code cells must:
- be short
- be readable
- have comments explaining intent
- load data relative to the notebook
- avoid clever abstractions

Code must not:
- assume Python fluency
- require debugging
- hide state changes
- perform API calls

If a code cell feels intimidating, simplify it.

---

## Data Loading Rules

All data loading must:
- use relative paths
- load from ./data/
- match the topic_slug filename

No hardcoded absolute paths.
No hidden downloads.
No implicit regeneration.

---

## Visualizations (If Present)

Visuals must:
- clarify, not decorate
- be interpretable without explanation
- avoid dense dashboards

Tables and text excerpts are preferred over complex charts.

---

## Teaching Posture (Critical)

Every notebook should feel like:
- a calm conversation
- not a lecture
- not a demo
- not a test

The notebook is a thinking partner, not a judge.

---

## Anti-Patterns (Explicitly Forbidden)

Notebooks must not:
- start with code
- require setup steps
- surprise users with cost
- assume technical background
- collapse nuance into conclusions
- chase novelty for its own sake

If a notebook feels impressive but confusing,
it has failed.

---

## Success Criteria

A notebook is successful if:
- a PM can use it without anxiety
- insights emerge naturally
- tooling fades into the background
- the user wants to explore further

If the notebook teaches *how to think* as well as *what to think about*,
it is doing its job.

---

End of document
