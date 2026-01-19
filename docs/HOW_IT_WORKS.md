# How It Works (No Wizards, Just Wires)

This repo isn’t “AI magic.” It’s a simple, repeatable pipeline that turns a messy pile of transcripts into something you can actually interrogate like a product person. The point is not to impress you. The point is to give you a workflow you can trust, debug, and reuse everywhere else you touch AI.

If you’ve ever used an LLM and thought “cool… but where did THAT come from?”, this doc is your antidote. It explains how we retrieve evidence first, then generate answers from that evidence, and then show citations so you can verify the claims instead of trusting the model’s confidence face.

## Overview

At a high level, there are three moving parts:

1) **Setup and indexing**  
We take the transcripts, split them into chunks, preserve the episode metadata, and store everything in a local vector database. This is where “trust” begins, because every chunk keeps its identity: which episode it came from, who the guest was, and when it happened.

2) **Retrieval**  
When you ask a question, we do a similarity search over that database and pull back the most relevant chunks. This is the moment where we decide what “evidence” the model is allowed to use.

3) **Synthesis with citations**  
We send the retrieved chunks to the model and ask it to produce a useful answer *grounded in those chunks*, then print the sources. The model is not supposed to freestyle. If it can’t point to receipts, it should say what’s missing.

Why this matters: this pipeline gives you **repeatability**. You can run the same query twice, change one knob, and learn what actually improved. That’s how PMs get leverage out of AI instead of just collecting shiny paragraphs.

## Quick Start

If you want the “just make it work” path, do this:

~~~bash
cd ~/<your code path>
git clone https://github.com/YOUR-USERNAME/lennysan-rag-o-matic
cd lennysan-rag-o-matic
./setup.sh
source ./activate.sh
python explore.py "What does Lenny say about pricing?"
deactivate
~~~

Notes:
- `./setup.sh` creates the environment and builds the index the first time.
- You usually do not need to run `index_corpus.py` manually unless you are rebuilding the index.

---

## CLI Commands

There are three main things you run from the command line: `setup.sh`, `index_corpus.py`, and `explore.py`.

### `setup.sh`
This is the “get me ready” script.
- Creates a local Python environment for this repo (so it doesn’t mess with your system)
- Installs the libraries the project needs
- Builds the vector index so searching can work

### `index_corpus.py`
This is the “turn transcripts into a searchable brain” step.
- Reads the YAML frontmatter (guest, title, date, URL)
- Breaks transcripts into chunks that are the right size to retrieve
- Stores embeddings + metadata in ChromaDB so we can retrieve with receipts

#### Why metadata matters
Every transcript has YAML frontmatter: guest, title, date, URL.  
We keep that metadata attached to every chunk so citations stay trustworthy and you can jump back to the original episode fast.

#### Bonus: the topic index
The `index/` folder (from upstream) contains tagged topic files.  
Use it as a discovery aid alongside RAG: browse topics, then ask better questions.

#### Basic usage

~~~bash
python index_corpus.py
~~~

#### Verbose controls

~~~bash
python index_corpus.py --verbose on
python index_corpus.py --verbose off
~~~

#### Rebuild the index (delete and re-run)

~~~bash
rm -rf data/chroma_db
python index_corpus.py
~~~

### `explore.py`
This is the part you actually use day-to-day.
- Finds the most relevant chunks for your question
- Sends those chunks to your chosen model
- Prints an answer plus sources so you can verify the claims

#### Basic query

~~~bash
python explore.py "What does Lenny say about pricing?"
~~~

#### Model switching

~~~bash
python explore.py --model haiku "What does Lenny say about pricing?"
python explore.py --model sonnet-4 "How do you find product-market fit?"
python explore.py --model gpt-4o-mini "Common enterprise sales mistakes?"
python explore.py --model gpt-4o "What are common enterprise sales mistakes?"
~~~

#### Web search fallback

~~~bash
python explore.py --web-search on "Why does SAFe suck?"
python explore.py --web-search always "Why does SAFe suck?"
python explore.py --web-search off "Why does SAFe suck?"
~~~

#### Docker search (one-off override)

~~~bash
python explore.py --web-search always --web-provider docker "Why does SAFe suck?"
~~~

#### Verbose controls

~~~bash
python explore.py --verbose on "Why does SAFe suck?"
python explore.py --verbose off "Why does SAFe suck?"
~~~

#### List available models

~~~bash
python explore.py --list-models
~~~

#### Order-insensitive flags (both work)

~~~bash
python explore.py "Why does SAFe suck?" --model gpt-4o
python explore.py --model gpt-4o "Why does SAFe suck?"
~~~

#### One-button Docker command

~~~bash
./scripts/docker_search.sh "Why does SAFe suck?"
SEARXNG_PORT=8081 ./scripts/docker_search.sh "Why does SAFe suck?"
~~~

## Output style (by design)

Answers follow this structure:
- Direct answer
- Indirect but relevant insights
- What’s missing

That last part is intentional: it makes gaps visible instead of hiding them behind confident prose.
