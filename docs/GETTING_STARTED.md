# Getting Started (Fast, Friendly, Real)

This is the “prove it works on my machine” doc. If you can copy/paste a few commands, you can go from zero to your first cited answer in minutes, without becoming a part-time Python mechanic.

The goal here is not elegance. The goal is momentum. You’ll install the basics, set one or two API keys, run setup, and ask your first question. If anything breaks, we route you to the exact doc that fixes that specific kind of pain.

One small mindset shift before you start: this tool is designed to give you **receipts, not vibes**. Under the hood it retrieves transcript evidence first, then asks your model to write an answer grounded in that evidence, then prints sources so you can verify the claims. You don’t need to understand the plumbing yet, but it helps to know what “done” looks like: an answer you can trust.

## Overview

There are only four moves in the “first run” dance:
1) clone the repo
2) set your API keys
3) run setup once to build the local index
4) ask a question and get an answer with sources

After you get the first win, you can start making it yours:
- set stable defaults in `docs/CONFIGURATION.md`
- enable optional web search in `docs/WEB_SEARCH.md`
- pull the ripcord in `docs/TROUBLESHOOTING.md` when gremlins appear

One important copy/paste note: this repo uses `~~~` fences for command examples embedded in a markdown document so the ChatGPT UI doesn’t mangle your snippets. If you see a code block in here, it should start with `~~~` and end with `~~~`.

---

## Prereqs (v0.9)
- Git
- Python 3.9+
- Anthropic API key (for Claude)
- OpenAI API key (only if using GPT models)

Optional:
- Docker Desktop (only for the v0.8 Docker search path)

## Quick Start

1) Clone the repo
~~~bash
git clone https://github.com/YOUR-USERNAME/lennysan-rag-o-matic
cd lennysan-rag-o-matic
~~~

2) Set your API keys
~~~bash
export ANTHROPIC_API_KEY='sk-ant-...'
export OPENAI_API_KEY='sk-...'  # optional
~~~

3) Run setup (one time)
~~~bash
chmod +x setup.sh activate.sh
./setup.sh
~~~

4) Choose your interface

**CLI** — ask a question, get a grounded answer with sources:
~~~bash
source activate.sh
python explore.py "What does Lenny say about pricing?"
~~~

**Browser** — same corpus, same models, no terminal required after setup:
~~~bash
source activate.sh
streamlit run app.py
~~~
Opens at `http://localhost:8501`. Pick your model, ask your question, download the answer as Markdown.

## Keeping the corpus fresh (v1.0)

New Lenny episodes don't appear automatically — you fetch them. No upstream dependency, no waiting for a PR to merge:

~~~bash
source activate.sh

# See what's new without writing anything
python fetch_corpus.py --dry-run

# Fetch new episodes (safe to run in batches)
python fetch_corpus.py --limit 6
python fetch_corpus.py             # gets the rest

# Re-index to pick them up
python index_corpus.py
~~~

Sync state is saved automatically between runs, so `--limit 6` always means "6 new ones I haven't fetched yet." See `deannotes/WHATS_NEW.v1.0.md` for the full flag reference.

## Next steps
- See `docs/CONFIGURATION.md` to set defaults
- See `docs/WEB_SEARCH.md` for web search options
- See `docs/TROUBLESHOOTING.md` if anything fails
