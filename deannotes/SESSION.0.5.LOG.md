# Session Log v0.5x (Prompts + Response Summaries)

Scope: From the first prompt in this Codex session (transition from Claude Desktop → Codex) through the prompt **"so wht is the plan for v0.6?"**.

Goal: capture verbatim prompts and Codex reasoning with Why‑not alternatives and PM lessons. Code diffs are summarized, not dumped.

## Prompts (verbatim) + Response Summaries

**Prompt**
```
Read AGENTS.md and README.md. Summarize: (1) golden path commands, (2) repo structure, (3) non-negotiables you must follow. Then wait.
```
**Response (summary)**
- Summarized golden path, repo map, and non‑negotiables to align with project governance.

**Why not**
- No code changes yet; this was an alignment step.

**PM lesson**
- Alignment before action prevents rework.

---

**Prompt**
```
read TRANSCRIPT_CLAUDE.md and TRANSCRIPT_README.md, these are the files from the original repo from which this repo was built. Tne re-read README.md and CLAUDE.md and AGENTS.md and RELEASE_v0.1.md and requirements.txt and then /deannotes/SESSION.0.1.STORY.md and explain to me what it means that we have accomplished with release v0.1
```
**Response (summary)**
- Interpreted v0.1 as a working proof‑of‑life RAG CLI with metadata preservation, cost transparency, and attribution.

**Why not**
- No new features; this was a retrospective explanation.

**PM lesson**
- Define “done” in human terms, not just code terms.

---

**Prompt**
```
What's the next release in our tactical plan?
```
**Response (summary)**
- Identified v0.5 as next release.

**Why not**
- No roadmap drift.

**PM lesson**
- Roadmap order is a product decision.

---

**Prompt**
```
What environtment variables do I need to make sure I have ready to go in my ~/.zshrc file?
```
**Response (summary)**
- Named required keys for v0.5 (Anthropic + OpenAI).

**Why not**
- No unnecessary keys.

**PM lesson**
- Reduce setup friction to the minimum viable checklist.

---

**Prompt**
```
no, for v0.5 you knucklehead
```
**Response (summary)**
- Corrected the answer quickly without defensiveness.

**Why not**
- No back‑and‑forth argument; just fix.

**PM lesson**
- Fast correction builds trust.

---

**Prompt**
```
okay, so what would be your plan for taking us from v0.1 to v0.5?
```
**Response (summary)**
- Proposed a tight plan: add `--model`, add OpenAI deps, update docs, test.

**Why not**
- No extra features beyond model switching.

**PM lesson**
- One‑feature releases need one‑feature plans.

---

**Prompt**
```
Explain to me th eoptions you'll be adding with the --model flag
```
**Response (summary)**
- Listed model options, then aligned with the canonical list.

**Why not**
- Avoided expanding the model list.

**PM lesson**
- Model choices are product decisions, not implementation details.

---

**Prompt**
```
shouldn't we have some less expensive models to choose from so we can use those for smoke tests?
```
**Response (summary)**
- Accepted the need for cheap smoke tests and prioritized low‑cost models.

**Why not**
- No extra models beyond the curated four.

**PM lesson**
- Cost‑sensitive testing is part of the UX.

---

**Prompt**
```
read index_corpus.py and explore.py and I think you'll see you're off-base with your plan.
```
**Response (summary)**
- Re‑aligned with actual code structure; added argparse + model factory.

**Why not**
- No assumptions about unimplemented behavior.

**PM lesson**
- The repo is the source of truth.

---

**Prompt**
```
read /deannotes/available-models.md to learn more about the available models.
```
**Response (summary)**
- Locked in the 4‑model list (haiku, sonnet‑4, gpt‑4o‑mini, gpt‑4o).

**Why not**
- No model sprawl.

**PM lesson**
- Constraints are strategic.

---

**Prompt**
```
if we type in pythong explore.py --model --help, can we get a listing ... or some similar convention?
```
**Response (summary)**
- Adopted argparse help conventions for discoverability.

**Why not**
- No custom help system.

**PM lesson**
- Standard UX beats bespoke UX.

---

**Prompt**
```
let's add `--list-models` as future iterations are going to be extended to both cloud-baed and local models.
```
**Response (summary)**
- Added `--list-models` as a future‑proofing hook.

**Why not**
- Still respected v0.5 scope (model switching only).

**PM lesson**
- Small hooks can unlock future features.

---

**Prompt**
```
we should test first, then document, don't you think?
```
**Response (summary)**
- Agreed: test before docs to avoid documenting assumptions.

**Why not**
- No doc‑first when behavior is unverified.

**PM lesson**
- Test before you narrate.

---

**Prompt**
```
this is my first time working with you, let's ee how you do with option 1.
```
**Response (summary)**
- Ran activation and tests; discovered missing deps and installed them.

**Why not**
- No skipping the install step.

**PM lesson**
- Testing reveals real friction.

---

**Prompt**
```
yes
```
**Response (summary)**
- Proceeded with dependency install and tests.

**Why not**
- No delay; explicit approval given.

**PM lesson**
- Respond quickly to explicit user intent.

---

**Prompt**
```
so Haiku gave me, ... Feels like we regressed badly.
```
**Response (summary)**
- Recognized regression in model behavior; adjusted prompt strategy.

**Why not**
- No “works for me” bias; optimize across models.

**PM lesson**
- Cross‑model robustness is part of quality.

---

**Prompt**
```
nope, nope, nope ... 4o, 4o-mini, Sonnet ... only haiku works
```
**Response (summary)**
- Further loosened prompt instructions to reduce refusals across models.

**Why not**
- Avoided provider‑specific hacks.

**PM lesson**
- Design for the weakest acceptable model.

---

**Prompt**
```
there ya go. let's update our .md and release notes, etc. in the release notes, you need to mention the issues we had with getting these prompts just right.
```
**Response (summary)**
- Updated docs and release notes to capture the prompt‑tuning saga.

**Why not**
- No undocumented behavior changes.

**PM lesson**
- The decision trail is part of the product.

---

**Prompt**
```
we should move `RELEASE_v0.1.md` and `RELEASE_v0.5.md` into a subdir named `releasenotes` -- then do option 1 about updating cost expectations in README.md -- then do option 2, adding "Troubleshooting model switching" section
```
**Response (summary)**
- Moved release notes, added cost table, added troubleshooting section.

**Why not**
- No scattered release files.

**PM lesson**
- Organization is usability.

---

**Prompt**
```
yes, definately update the link refrences -- good catch -- thanks for being proactive
```
**Response (summary)**
- Updated release note links after moving files.

**Why not**
- No broken documentation links.

**PM lesson**
- Doc hygiene builds credibility.

---

**Prompt**
```
Hey, went to run the test manually. activate.sh has some undesired behvior. basically I run the command, but then it doesn't leave us in the virtual environment. so of course none of the python commands work.
```
**Response (summary)**
- Diagnosed sourced vs executed script behavior; added guardrails.

**Why not**
- No assumption that users will source correctly.

**PM lesson**
- Scripts are part of UX.

---

**Prompt**
```
that dumped me straight out of my termal, here's a capture: ```deanpeters@MacBookPro lennysan-rag-o-matic % source activate.sh
⚠️  This script must be sourced to keep the environment active.
Run: source activate.sh

Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[Process completed]
```
```
**Response (summary)**
- Fixed detection for zsh; prevented terminal exit.

**Why not**
- Avoided shell‑specific landmines.

**PM lesson**
- UX must survive real shells, not just ideal ones.

---

**Prompt**
```
First, let's update our activate.sh with comments explaining what the file and why it's needed to run the python scripts this way.
```
**Response (summary)**
- Added pedagogic comments to activate.sh.

**Why not**
- No silent scripts; PMs need context.

**PM lesson**
- Teaching is part of the product.

---

**Prompt**
```
we should explain in that same file why running in a virtual environment is important. Remember, this repo has a primary objective of being pedagoic, that is, to teach less technical product managers how to work with repos like this.
```
**Response (summary)**
- Expanded activate.sh with beginner‑friendly explanation.

**Why not**
- No purely technical comments; keep it human.

**PM lesson**
- Pedagogy beats cleverness.

---

**Prompt**
```
we should test first, then document, don't you think?
```
**Response (summary)**
- Reaffirmed test‑before‑docs principle.

**Why not**
- Avoided doc drift.

**PM lesson**
- Process discipline is part of shipping.

---

**Prompt**
```
I think I need a grep command I can use to interrogate the Claire Vo corpus or our data for terms that don't exist. something like `cd ... && grep "<dean puts in term>" -i<and other args>`
```
**Response (summary)**
- Provided `rg` and `grep` commands for fast corpus checks.

**Why not**
- No custom search tool; leverage standard CLI.

**PM lesson**
- Meet users where they are: simple tools first.

---

**Prompt**
```
update our documentation first. then push as v0.62
```
**Response (summary)**
- Updated docs then tagged v0.62.

**Why not**
- No tag before documentation accuracy.

**PM lesson**
- Releases are public contracts.

---

**Prompt**
```
so wht is the plan for v0.6?
```
**Response (summary)**
- Transitioned to v0.6 planning: CONFIGS.yaml only.

**Why not**
- No features beyond configuration in v0.6.

**PM lesson**
- Finish one release before opening the next.

