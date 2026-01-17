# Weekend at Lenny’s v0.5

## Part 2: The Model Switch That Bit Back (In a Good Way)

**TL;DR:** We shipped v0.5 model switching, added a pedagogic 3‑part answer format (Direct / Inferred / Missing), and learned that GPT‑4o and Sonnet can be *too* polite unless you explicitly give them permission to be useful.

**Time (ET):** ~4:15 PM → ~6:00 PM  
**Role:** Product Manager (Recovering Engineer)  
**Tooling:** Codex + terminal + venv + a small chorus of model personalities  
**Goal:** Ship `v0.5` model switching without breaking the “one feature per version” rule.

---

## Prologue: Football, fate, and feature flags

Embittered by the Ravens’ fall‑apart‑season, and spared from watching my Pittsburgh‑born Steelers miss the picture entirely, I opted to play with models instead of watching the Bills vs Broncos. Especially since the Broncos are my older brother’s favorite team. (No, I’m not jealous, but why does his team get to win when mine and my wife’s don’t?) …Clearly the fix is in, but I digress.

At 4:15 PM, I opened the repo and told myself the lie we all tell:

```
This is one feature. It’ll be fast.
```

Spoiler: it was fast. It just wasn’t simple.

---

## 4:17 PM — The model list reset (aka: read the docs)

We started with the most PM thing possible: **read the existing notes**.

```
read /deannotes/available-models.md to learn more about the available models.
```

Then came the “please don’t improvise” correction:

```
read index_corpus.py and explore.py and I think you'll see you're off-base with your plan.
```

That line set the tone: the repo already knows the truth. The job is to align with it.

We needed four models. Not ten. Not twenty. Four:

- `haiku`
- `sonnet-4`
- `gpt-4o-mini`
- `gpt-4o`

**Lesson:** The docs are the product. And the docs already wrote the spec.

---

## 4:22 PM — The CLI grows a brain

We agreed the CLI should explain itself. That meant better `--help` behavior and a way to list models without digging into code.

```
if we type in python explore.py --model --help, can we get a listing ... or some similar convention?
```

Then you made the long‑view call:

```
let's add `--list-models` as future iterations are going to be extended to both cloud-baed and local models.
```

Translation: “Design for future‑you without breaking present‑you.”

---

## 4:28 PM — Testing before docs (a rare act of discipline)

```
we should test first, then document, don't you think?
```

Yes. Absolutely. And we did.

We tried to run:

```
python explore.py --list-models
```

…and hit the first wall:
- `python` not on PATH
- venv not active
- missing deps

You handed me the test baton:

```
this is my first time working with you, let's ee how you do with option 1.
```

We activated the venv, then discovered OpenAI deps weren’t installed. So we installed them. (Also learned pip can’t download without network access.)

Finally:

```
python explore.py --list-models
```

…and the list printed. Confidence returned. Snack queue re‑opened.

---

## 4:38 PM — The “CONFIG.yaml” temptation

The instinct to centralize configuration came fast:

```
feels like we should have a CONFIG.yaml file for stuff like this.
```

We parked it to v0.6, because v0.5 is one feature. Discipline isn’t fun, but it’s cheaper than regret.

**Lesson:** If you can’t say “no” to a good idea, you can’t ship.

---

## 4:42 PM — The activation script that evicted the user

You ran:

```
source activate.sh
```

…and the shell **exited**. Total face‑plant.

Capture:

```
⚠️  This script must be sourced to keep the environment active.
Run: source activate.sh

Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[Process completed]
```

Turns out my “sourced” detection was bash‑centric and offended zsh. We fixed it and moved on.

**Lesson:** Any script that touches the shell is a loaded weapon.

---

## 4:55 PM — The OpenAI “I’m sorry Dave” era

You ran the same query across models:

```
What are common enterprise sales mistakes?
```

Haiku gave a useful answer. Sonnet gave a partial one. GPT‑4o and GPT‑4o‑mini shrugged:

```
The context provided does not directly address…
```

It was the same retrieval, the same chunks, the same corpus — but wildly different behavior.

You called it:

```
technically it works, but the outcomes for OpenAI suck when compared to Anthropic.
```

**Lesson:** Model switching is easy. Model behavior is not.

---

## 5:05 PM — Two fixes, one goal

We agreed to do **both**:

```
I think both improvements are called for, let's do it.
```

So we:
- Added MMR + higher `k` / `fetch_k` to diversify context
- Added a pedagogic response structure (Direct / Inferred / Missing)

---

## 5:12 PM — The prompt tuning saga (aka: diplomacy with robots)

We tried a strict version. It made Sonnet and GPT defensive.

We tried a rigid 3‑line format. It got worse.

Then you called the regression:

```
crap, now GPT-4o isn't finding direct, it was just before this fix. and gpt-4o-mini also now not finding direct. Feels like we regressed badly.
```

We loosened it.

```
nope, nope, nope ... 4o, 4o-mini, Sonnet ... only haiku works
```

We loosened it again.

```
there ya go.
```

Final structure:

~~~
Direct answer:
Indirect but relevant insights (inferred):
What's missing:
~~~

The key change: **best‑effort direct answer grounded in context**, even when the context is thin.

**Lesson:** We didn’t weaken truth. We stopped punishing usefulness.

---

## 5:35 PM — Documentation as a deliverable

Once behavior stabilized, you insisted on the paper trail:

```
let's update our .md and release notes, etc. in the release notes, you need to mention the issues we had with getting these prompts just right.
```

Then:

```
we should move RELEASE_v0.1.md and RELEASE_v0.5.md into a subdir named releasenotes
```

Then:

```
yes, definately update the link refrences -- good catch -- thanks for being proactive
```

**Lesson:** A fix that isn’t documented isn’t a fix. It’s a rumor.

---

## 5:45 PM — Pedagogy wins (again)

We committed to the purpose of the tool:

```
I like this 3 part structure, as this is primarily a pedagogic tool, and secondarily a research tool.
```

That line is the thesis of v0.5.

---

## What shipped in v0.5 (and why it matters)

- `--model` flag (Anthropic + OpenAI)
- `--list-models` helper
- 4 curated models
- Model‑specific API key validation
- MMR retrieval + higher `k`
- Pedagogic response format (direct / inferred / missing)

One feature. One release. Many lessons.

---

## What didn’t ship (and why)

- CONFIGS.yaml → v0.6
- Web fallback → v0.75
- Notebooks → v1.0

Focus on less. Sleep on more.

---

## PM‑style takeaways (from a tired PM)

1) Model switching is easy. Model behavior isn’t.  
2) Pedagogy beats perfection for this audience.  
3) If a model refuses, the prompt is usually the bug.  
4) Docs are the support team you don’t have.  
5) Anything touching the shell must be treated like production.

---

✅ v0.5 shipped. Now go drink water and stop touching the prompt.
