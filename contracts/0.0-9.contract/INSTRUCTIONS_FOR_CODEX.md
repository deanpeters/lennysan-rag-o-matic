# Instructions for Codex and Claude Code (v0.x)
INSTRUCTIONS_FOR_CODEX.md

This file governs how you implement and modify Version 0.x of this repository.

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

## What You Are Building (0.x)

You are maintaining a CLI-first RAG tool that:
- preserves metadata end-to-end
- provides clear attribution
- keeps setup and usage low-barrier
- exposes costs and configuration

You are not building notebooks, dashboards, or agentic workflows in 0.x.

---

## Non-Negotiables

- Preserve YAML frontmatter metadata end-to-end.
- Never weaken source attribution (guest/title/date/URL).
- Keep setup and usage low-barrier for non-technical PMs.
- Track and communicate costs (embeddings + LLM + web search).
- Maintain "one feature per version" scope discipline.
- Update docs before tagging releases.

---

## Configuration Rules

- CONFIGS.yaml is the single source of truth for non-secret config.
- Environment variables are for secrets only.
- Do not introduce new config files.
- CLI flags may override defaults but must not hide them.

If you need a new config value:
- add it to CONFIGS.yaml
- update README usage
- note it in releasenotes

---

## Web Search Rules (v0.75+)

- Web search is a fallback, not a primary interface.
- AUTO uses conservative heuristics to protect quota.
- ALWAYS exists for testing and manual override.
- If API key is missing, disable search and warn clearly.
- Never imply a web search happened if it did not.

---

## Prompt and Output Discipline

- Keep the Direct / Indirect / Missing structure.
- If a model regresses, document and prefer stable behavior.
- Avoid long, unstructured answers.
- Always print sources with attribution.

---

## Files You Must Not Break

You must not rename, repurpose, or break:
- explore.py
- index_corpus.py
- episodes/
- index/
- releasenotes/ history

All work must be additive.

---

## Markdown Fence Rule

If a Markdown document contains embedded Markdown examples:
- the embedded examples must use a different fence type

Rule:
- outer document uses ```markdown
- embedded examples use ~~~markdown

This rule is mandatory.

---

End of document
