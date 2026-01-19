# LennySan RAG-o-Matic

~~~text
 _                                  ____
| |    ___ _ __  _ __  _   _       / ___|  __ _ _ __
| |   / _ \ '_ \| '_ \| | | |_____ \___ \ / _` | '_ \
| |__|  __/ | | | | | | |_| |_____| ___) | (_| | | | |
|_____\___|_| |_|_| |_|\__, |      |____/ \__,_|_| |_|
                       |___/
 ____      _    ____               __  __       _   _
|  _ \    / \  / ___|___          |  \/  | __ _| |_(_) ___
| |_) |  / _ \ | |  _  _ \ _____  | |\/| |/ _` | __| |/ __|
|  _ <  / ___ \| |_| |_| |_____|  | |  | | (_| | |_| | (__
|_| \_\/_/   \_\____\___/         |_|  |_|\__,_|\__|_|\___|
                                                       v0.75
~~~
A low-barrier, learn-by-building PM pm research tool for exploring Lenny Rachitsky's 320+ podcast episodes using AI and RAG from the CLI, with future support for Jupyter notebooks, time-series exploration, and more.

## What This Does

You know that moment when you *swear* Lenny said something perfect about pricing, strategy, hiring, or “stop shipping roadmap confetti”… and now you’re scrolling episode pages like a raccoon in a dumpster. This repo fixes that. It’s a learn-by-building PM research tool that lets you query 320+ Lenny podcast transcripts from the CLI using RAG, get an answer you can actually use, and see exactly which episodes the answer came from. Receipts, not vibes.

## What you can do in 5 minutes

This is the proof-of-life path. Setup once, activate the environment, ask a question like a human, get a grounded answer with sources, and immediately feel your brain rehydrate.

~~~bash
./setup.sh
source activate.sh
python explore.py "What does Lenny say about pricing?"
~~~



## Why this exists

Most “AI for PM” stuff is tool tourism, demo theater, or magical thinking. This repo is practice. It teaches the workflow you actually need in 2026: retrieval, traceability, cost discipline, and the ability to say, “Cool claim. Show me the receipts.” Use it to learn RAG by doing, on a corpus that’s genuinely worth searching.

## How it works (the honest version)

You ask a question. The tool retrieves the most relevant transcript chunks from a local vector database. Then your chosen model synthesizes an answer grounded in those chunks and prints citations so you can verify where the ideas came from. Output is intentionally structured as: direct answer, adjacent insights, and what’s missing, because gaps should be visible, not buried under confident prose.

If you want the wiring diagram without wizard robes: `docs/HOW_IT_WORKS.md`.

## The docs are the product

This README is the front door. The docs are the house. Each one exists because it answers a real PM question like “how do I start fast,” “how do I not accidentally spend money,” or “why is Docker screaming at me.” These are not compliance docs. They’re the curriculum.

### docs/GETTING_STARTED.md

This is the “value before your coffee gets cold” path. It gets you from clone to first cited answer with the fewest moving parts, the fewest opportunities for your machine to become an obstacle course, and the most respect for your time. If the repo is going to earn your trust, it earns it here. ☞  [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

### docs/HOW_IT_WORKS.md

This is the “no wizards, just wires” explanation of the system. It shows the three moving parts, why metadata is non-negotiable, how the retrieval-to-answer loop works, and why the output format is designed to make gaps obvious. Read it once and you’ll be better at using every AI tool you touch, not just this repo. ☞  [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md).

### docs/CONFIGURATION.md

This is how you change behavior without changing code. `CONFIGS.yaml` is the single source of truth for defaults, which means you can tune model choice, retrieval behavior, and web-search knobs like a sane product person instead of a sleep-deprived spelunker. CLI flags override anything at runtime, but this doc is how you make “your normal” stable and repeatable. ☞  [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

### docs/WEB_SEARCH.md

This is optional power with a safety latch. Web search only runs when you explicitly enable it, and this doc explains when it triggers, which provider you’re using, and what tradeoffs you’re accepting when you let “the internet” into your answer loop. It also gives you the escape hatch: if web search gets annoying, turn it off and keep learning. ☞  [docs/WEB_SEARCH.md](docs/WEB_SEARCH.md).

### docs/DOCKER_SEARCH.md

This is the advanced path for running a local search backend via Docker, delivered the only acceptable way: one button, no drama. It tells you how to run it, how to change ports, and how to recover when Docker does that thing where it pretends it’s the main character. Useful, powerful, occasionally fussy. Like many senior stakeholders. ☞  [docs/DOCKER_SEARCH.md](docs/DOCKER_SEARCH.md).

### docs/COSTS.md

This is the adult supervision doc. It tells you what actually costs money, what costs almost nothing, and how to keep experiments cheap enough to stay fun. If you’ve ever looked at an AI bill and felt your soul leave your body, read this before you start cranking knobs. ☞ [docs/COSTS.md](docs/COSTS.md).

### docs/TROUBLESHOOTING.md

This is the antidote to spiraling. Missing keys, wrong model provider, too much output, Docker weirdness, “python not found,” setup failures, the usual gremlins. It’s written for PMs who want fixes, not a surprise graduate degree in toolchains. ☞ [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

### docs/ROADMAP.md

This is how we avoid scope creep, thrash, and “just one more feature” death spirals. One focused capability per version, with a clear runway from proof-of-life to notebooks and beyond. If you want to understand what’s next without starting a religion over it, this is the file. ☞ [docs/ROADMAP.md](docs/ROADMAP.md).

### docs/RELEASES.md

This is the human-readable history of what shipped and where to find the details. It points you to release notes and the PM-friendly “what’s new” narrative, so you can track capability changes without spelunking commits like an archaeologist. ☞ [docs/RELEASES.md](docs/RELEASES.md).

### docs/CONTRACTS_AND_LOGS.md

This is where the repo becomes a teaching tool instead of “some scripts.” Contracts capture intended behavior so the tool doesn’t drift into accidental chaos. Session logs capture the real decisions and tradeoffs, so you can learn from the work, not just admire the outcome. If you care about trust, traceability, and governance, this is the spine. ☞ [docs/CONTRACTS_AND_LOGS.md](docs/CONTRACTS_AND_LOGS.md).

### docs/DECISIONS.md

This is the decision log for big bets only. It exists so future you doesn’t have to play detective, and so contributors don’t accidentally relitigate the same core choices every few weeks. If a change affects trust, cost, or behavior, it belongs here with the “why” written down. ☞ [docs/DECISIONS.md](docs/DECISIONS.md).

## Current status: v0.75

Today it’s CLI-first and Mac-first. It supports model switching across Anthropic and OpenAI, uses `CONFIGS.yaml` for defaults, and supports optional web-search fallback modes. It’s intentionally a weekend-grade product: useful, teachable, and still a little rough around the edges.

## Credits

The podcast content belongs to Lenny Rachitsky. The transcript corpus is built on Claire Vo’s [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts) gift to the PM community. This repo is the PM learning layer on top: the CLI workflow, the retrieval loop, and the insistence that every answer earns its confidence with citations.
