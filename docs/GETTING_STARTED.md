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

## Prereqs (v0.75)
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

3) Run setup
~~~bash
chmod +x setup.sh activate.sh
./setup.sh
~~~

4) Ask a question
~~~bash
source activate.sh
python explore.py "What does Lenny say about pricing?"
~~~

## Want to keep in sync with upstream?
See `GITLENNY.md` for fork + sync instructions.

## Next steps
- See `docs/CONFIGURATION.md` to set defaults
- See `docs/WEB_SEARCH.md` for web search options
- See `docs/TROUBLESHOOTING.md` if anything fails
