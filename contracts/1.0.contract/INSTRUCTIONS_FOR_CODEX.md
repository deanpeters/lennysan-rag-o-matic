# Instructions for Codex and Claude Code
INSTRUCTIONS_FOR_CODEX.md

This file governs how you implement Version 1.0 of this repository.

It is a binding execution contract.
If your generated code conflicts with this file, your output is wrong.

This repository is a pedagogic tool first, and a practical research tool second.
Both priorities matter.
The implementation must remain simple, safe, and teachable.

---

## Required Reading Order (Do Not Skip)

Before writing any code, read these files in order:

1. README.md
2. RELEASE_NOTES.md
3. 00-consistency-check.md
4. 01-repo-reality-and-scope.md
5. 02-user-journey.md
6. 03-constitution.md
7. 04-implementation-brief.md
8. 05-user-experience-pack.md

If there is a conflict:
- 03-constitution.md wins
- 02-user-journey.md defines UX intent
- 04-implementation-brief.md defines what to build

---

## What You Are Building

You are implementing topic-based notebooks as a stable learning and research interface.

A user must be able to run:

~~~text
python create_topic.py "why safe sucks"
~~~

This must create a ready-to-open topic kit:
- a notebook with orientation and guided exploration
- a prepared dataset created at build-time using API calls
- a manifest describing provenance

---

## Build-Time vs Learn-Time (Non-Negotiable)

Enforce a strict separation.

### Build-Time
Occurs when running:
~~~text
python create_topic.py "<topic>"
~~~

At build-time:
- API calls are allowed and expected
- data is generated and written to disk
- cost is incurred intentionally
- progress is printed in plain language

Build-time responsibilities belong to:
- create_topic.py
- build_topic_data.py

### Learn-Time
Occurs when the user opens and runs the notebook.

At learn-time:
- no API calls are allowed by default
- no data regeneration is allowed by default
- the notebook reads prepared files only
- Run -> Run All must be safe and repeatable

If a notebook can accidentally incur cost, the implementation violates this contract.

---

## Locked Structure (Do Not Invent Alternatives)

Each topic is a self-contained kit:

~~~text
notebooks/<topic_slug>/
  <topic_slug>.ipynb
  data/
    <topic_slug>.jsonl
    manifest.json
~~~

Rules:
- one notebook per topic
- one primary dataset per topic
- dataset filename matches topic_slug
- no numeric prefixes
- no parallel data directories

---

## Configuration Rules (Non-Negotiable)

- CONFIGS.yaml is the single source of truth for non-secret configuration
- environment variables are used for secrets only
- do not hardcode model names, temperature, tokens, or limits
- do not introduce new config files

If you need a new config value:
- add it minimally to CONFIGS.yaml
- keep it readable
- document why in releasenotes

---

## Files You May Create

You may create:

- create_topic.py
- build_topic_data.py
- config_loader.py
- scripts/build_topics_batch.sh
- a notebook boilerplate template (mechanism is your choice)

---

## Files and Areas You Must Not Break

You must not rename, repurpose, or break:

- explore.py
- index_corpus.py
- episodes/
- index/
- existing releasenotes history

All work must be additive.

---

## Behavioral Requirements

### create_topic.py

Must:
- accept a topic name as CLI input
- generate a deterministic topic_slug
- check for an existing topic kit
- recommend reuse if it exists
- avoid overwriting without confirmation
- call build_topic_data.py for all API work
- generate notebook from the canonical boilerplate
- print a copy-paste command to open the notebook

Must not:
- open the notebook automatically
- require manual edits to configuration files
- leave partial state on failure

---

### build_topic_data.py

Must:
- perform all API calls required for dataset creation
- reuse existing episodes/ and index/ data
- generate a bounded dataset suitable for learning and research
- write outputs to:
  - notebooks/<topic_slug>/data/<topic_slug>.jsonl
  - notebooks/<topic_slug>/data/manifest.json

Must not:
- re-index the corpus
- mutate canonical data
- depend on notebook execution

---

### Notebooks

Notebooks must:
- start with the canonical orientation cell from 05-user-experience-pack.md
- assume no Python knowledge
- load CONFIGS.yaml via config_loader.py
- load data relative to themselves:
  - ./data/<topic_slug>.jsonl
  - ./data/manifest.json
- run top-to-bottom safely
- avoid API calls during normal execution
- avoid data regeneration during normal execution

If any notebook cell might incur cost during Run All, remove it.

---

## Progress and Logs

The user-facing output from scripts must be:
- plain language
- minimal but reassuring
- explicit about where outputs were written

Technical logs may be written under logs/ if needed.

---

## Markdown Fence Rule (Critical)

If you write Markdown that contains embedded Markdown examples:
- embedded examples must use a different fence type

Rule:
- outer document uses ```markdown
- embedded examples use ~~~markdown

Violations must be corrected.

---

## Definition of Done

Implementation is complete when:

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
   - runs top-to-bottom
   - provides guided exploration and evidence

3. Existing functionality continues to work

4. Batch script can generate multiple topics reliably

If the solution feels clever, stop and simplify.

---

End of instructions
