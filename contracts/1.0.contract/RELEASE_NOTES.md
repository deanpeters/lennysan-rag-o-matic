# Release Notes – Version 1.0
RELEASE_NOTES.md

Version 1.0 establishes the contractual foundation for this repository.

This is a futuristic look of what the product manager envisions.

It defines a stable learning and research interface for Product Managers,
along with explicit governance for how the system is built, used, and evolved.

This release is about intent and trust, not feature volume.

---

## What Version 1.0 Represents

Version 1.0 is a commitment to clarity.

It means:
- the user experience is intentional
- the structure is deliberate
- the rules are explicit
- change will be conscious, not accidental

Version 1.0 does not mean the system is finished.
It means it is stable enough to teach from, build on, and share.

---

## What Shipped in 1.0

### Topic-Based Notebooks (Core Interface)

The primary learning and research interface is now topic-based notebooks.

Each topic is a self-contained kit:
- one notebook
- one prepared dataset
- one manifest describing how the data was created

Topics live at:

- notebooks/<topic_slug>/<topic_slug>.ipynb

This structure is intentional and governed.

---

### One-Command Topic Creation

New topics can be created with a single command:

~~~text
python create_topic.py "your topic here"
~~~

This command:
- normalizes the topic name
- checks for existing work
- performs required API calls up front
- prepares a bounded dataset
- creates a ready-to-open notebook
- avoids surprise costs later

Topic creation is explicit.
Learning is safe.

---

### Strict Separation of Build-Time and Learn-Time

Version 1.0 introduces a hard boundary between:

**Build-Time**
- API calls are allowed
- data is generated
- cost is incurred intentionally
- outputs are written to disk

**Learn-Time**
- notebooks read prepared files only
- no API calls are made
- no data regeneration occurs
- “Run All” is safe and repeatable

This separation protects trust and pedagogy.

---

### Self-Contained Topic Kits

Each topic folder contains everything needed to learn or share:

- the notebook
- the derived dataset
- a manifest with provenance

This enables:
- zip-and-go sharing
- clean pull requests
- forking a topic into its own project
- community reuse without setup friction

---

### Configuration Discipline

Version 1.0 reinforces strict configuration governance:

- CONFIGS.yaml is the single source of truth
- environment variables are used for secrets only
- no hidden or duplicated configuration
- no hardcoded model or parameter values

Experimentation remains visible and intentional.

---

## What Did Not Change

Version 1.0 does not replace or redesign:

- the existing CLI exploration flow
- the indexing pipeline
- the episode transcript corpus
- explore.py or index_corpus.py

All existing workflows continue to function.

This release is additive, not disruptive.

---

## Why This Release Exists

Earlier versions surfaced important learnings:

- prompt phrasing matters
- model and temperature choices affect outcomes
- ad-hoc experimentation is expensive
- setup friction discourages thoughtful exploration

Version 1.0 responds by:
- front-loading cost into explicit build steps
- separating setup from learning
- making reuse the default
- replacing “vibe coding” with governance

---

## Who Version 1.0 Is For

This release is for Product Managers who:

- want to explore real product management questions
- value evidence over hot takes
- are curious but cautious about technical tools
- want reproducible thinking, not just outputs

Deep technical expertise is not required.

---

## Known and Intentional Limitations

Version 1.0 intentionally excludes:

- multi-topic notebooks
- live data refresh inside notebooks
- notebook orchestration systems
- dashboards or automation frameworks
- advanced visualization pipelines

These were excluded to protect clarity and learning flow.

---

## What Success Looks Like

Version 1.0 is successful if:

- a PM can create or reuse a topic in minutes
- notebooks feel safe and understandable
- users focus on the topic, not the tooling
- sharing work feels low-risk
- contributors understand the rules before coding

If the system teaches judgment and reduces accidental complexity,
it is doing its job.

---

## Looking Forward

Future releases may explore:
- opt-in data refresh mechanisms
- richer exploration patterns
- curated topic collections
- deeper community contribution models

Any such changes will be evaluated against the 1.0 contract
before being introduced.

---

End of release notes
