# Implementation Brief
04-implementation-brief.md

This document defines exactly what must be implemented for Version 1.0
and how that implementation must behave.

It translates the Constitution and User Journey into concrete,
testable execution rules.

If implementation decisions conflict with this brief,
the implementation is wrong.

---

## Scope of Version 1.0 Implementation

Version 1.0 introduces a new, governed learning and research interface.

Specifically:
- topic-based notebooks
- self-contained topic kits
- explicit build-time data generation
- safe, repeatable notebook execution

Version 1.0 does not redesign or replace existing systems.

All work must be additive.

---

## Canonical User Action

From the repository root, a user can run:

~~~text
python create_topic.py "why safe sucks"
~~~

This action must result in:

- intentional API calls at build-time
- a prepared dataset written to disk
- a notebook created from a canonical boilerplate
- no further setup steps required
- a clear instruction for opening the notebook

This action defines success for Version 1.0.

---

## Build-Time Responsibilities (Explicit)

Build-time occurs only when a user explicitly runs topic creation.

Build-time responsibilities include:
- performing all API calls
- generating derived datasets
- incurring compute cost intentionally
- writing outputs deterministically
- printing clear progress messages

Build-time code must live in:
- create_topic.py
- build_topic_data.py

Build-time must never occur implicitly.

---

## Learn-Time Responsibilities (Explicit)

Learn-time occurs when a user opens and runs a notebook.

At learn-time:
- no API calls are allowed by default
- no dataset regeneration is allowed
- notebooks read prepared files only
- execution must be safe and repeatable

If “Run All” can incur cost or change state,
the implementation violates this brief.

---

## Required Directory Structure

All new files introduced by Version 1.0 must conform to:

~~~text
/
├─ create_topic.py
├─ build_topic_data.py
├─ config_loader.py
├─ CONFIGS.yaml
├─ notebooks/
│  └─ <topic_slug>/
│     ├─ <topic_slug>.ipynb
│     └─ data/
│        ├─ <topic_slug>.jsonl
│        └─ manifest.json
├─ scripts/
│  └─ build_topics_batch.sh
├─ logs/
~~~

Rules:
- one notebook per topic
- one primary dataset per topic
- dataset filename matches topic_slug
- topic folders are self-contained
- no numeric prefixes
- no alternative layouts

---

## Configuration Rules

CONFIGS.yaml is the single source of truth for non-secret configuration.

All code must:
- read configuration via config_loader.py
- use environment variables for secrets only
- avoid hardcoded models or parameters
- avoid duplicated configuration logic

Configuration changes require contract awareness.

---

## Script Responsibilities

### create_topic.py

create_topic.py is the primary orchestration entry point.

It must:
- accept a topic name via CLI
- generate a deterministic topic_slug
- detect existing topic kits
- recommend reuse when appropriate
- avoid overwriting without confirmation
- call build_topic_data.py for all API work
- create the topic directory structure
- generate the notebook from the canonical boilerplate
- print a copy-paste command to open the notebook

It must not:
- open notebooks automatically
- perform analysis itself
- hide cost-incurring steps
- leave partial state on failure

---

### build_topic_data.py

build_topic_data.py performs all dataset creation.

It must:
- read configuration via config_loader.py
- reuse episodes/ and index/ as canonical sources
- generate a bounded, useful dataset
- write outputs to:
  - notebooks/<topic_slug>/data/<topic_slug>.jsonl
  - notebooks/<topic_slug>/data/manifest.json

manifest.json must include:
- topic title
- topic slug
- creation timestamp
- model used
- temperature used
- prompt identifier or version
- item count

It must not:
- re-index the corpus
- mutate canonical data
- depend on notebook execution

---

## Notebook Generation Rules

Notebooks must be generated from a canonical boilerplate.

Every notebook must:
- begin with orientation and reassurance
- explain how to use the notebook
- assume no Python knowledge
- load data relative to itself
- run top-to-bottom without setup steps
- avoid API calls during normal execution
- avoid data regeneration during normal execution

Notebook behavior is governed, not optional.

---

## Batch Script (Verification Tool)

scripts/build_topics_batch.sh exists to:
- generate multiple topics
- validate repeatability
- surface failures early

It is a verification aid, not a production system.

---

## Progress Reporting and Logs

User-facing output must:
- be plain language
- be explicit about actions and outcomes
- indicate where files are written

Technical logs may be written under logs/.

Users must never wonder what just happened.

---

## Markdown Fence Rule

If a Markdown document contains embedded Markdown examples:
- the embedded examples must use a different fence type

Rule:
- outer document uses ```markdown
- embedded examples use ~~~markdown

This rule is mandatory.

---

## Definition of Done

Version 1.0 implementation is complete when:

1. Running:
   ~~~text
   python create_topic.py "why safe sucks"
   ~~~
   creates:
   - notebooks/safe_sucks/safe_sucks.ipynb
   - notebooks/safe_sucks/data/safe_sucks.jsonl
   - notebooks/safe_sucks/data/manifest.json

2. The notebook:
   - opens with clear instructions
   - runs top-to-bottom safely
   - supports guided exploration and evidence review

3. Existing CLI and indexing workflows still function

4. Batch script can generate multiple topics reliably

If the solution feels clever, stop and simplify.

---

End of document
