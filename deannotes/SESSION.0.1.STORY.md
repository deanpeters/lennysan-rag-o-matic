# How I Built a RAG System in One Night (Using Claude as My Co-Pilot)

*A case study in progressive AI collaboration: From concept on mobile to shipped code via CLI*

## The Setup

It's 3 AM. I'm lying in bed, thinking about Lenny Rachitsky's podcast corpus. 

Three hundred twenty episodes. Thousands of insights about pricing, growth, product-market fit, enterprise sales. All locked up in transcripts that are a pain in the ass to search through.

ChatPRD already did the hard work—they transcribed everything, Claire Vo enriched it with metadata. But I still have to rebuild my context in Claude Projects every time I want to explore a topic. That's annoying.

What if I could just... query it? Command line. Local. My terms.

I pull out my phone and start a conversation with Claude.

## Act One: Concept (On My Phone)

**Me:** "I want to build a RAG tool for Lenny's podcast corpus. Fork the ChatPRD repo, add ChromaDB, CLI query tool. Call it LennySan RAG-o-Matic. What's the simplest possible v0.1?"

This is key: I'm not asking Claude to build it. I'm asking it to help me *think* about building it.

Claude comes back with: "Proof of life. One CLI tool. Claude Haiku. Mac only. Ship ONE feature: make queries work."

Yes. This is the discipline. No Jupyter notebooks. No Streamlit UI. No model switching. Just get the damn thing working.

We sketch out a roadmap. Each version = one feature. No bundling. No scope creep.

- v0.1: CLI works
- v0.5: Model switching
- v1.0: Jupyter
- v2.0: Streamlit
- v3.0: Windows
- v4.0: Local LLMs

I'm still in bed. Phone in hand. But now I have a plan.

## Act Two: Architecture (Desktop App)

Morning. Coffee. I switch to Claude Desktop.

Now we get into the details. This is where Claude shines—not replacing my judgment, but accelerating my exploration of options.

**Me:** "What vector database? I don't want vendor lock-in or cloud accounts."

**Claude:** "ChromaDB. Local, open source, no cloud account needed."

**Me:** "Embeddings?"

**Claude:** "sentence-transformers/all-MiniLM-L6-v2. Free, runs locally, no API costs."

**Me:** "Cost per query?"

**Claude:** "Claude Haiku: $0.001-0.005 per query. Pennies."

See what's happening here? I'm making the strategic calls. Claude is doing the research. It's like having a really fast junior PM who can read documentation instantly.

But here's the critical decision: **metadata preservation**.

The ChatPRD transcripts have YAML frontmatter—guest name, title, date, keywords, YouTube URLs. This is gold. Claire Vo did real work here.

**Me:** "Can we preserve that metadata in the vector store?"

**Claude:** "Yes. Parse YAML separately, attach to each chunk, ChromaDB stores it, retrieval returns it."

This changes everything. Now every answer comes with attribution: which episode, which guest, when it was recorded. That's not just nice—that's *trust*. That's the difference between a toy and a tool.

We document this decision in CLAUDE.md. Future me (or future contributors) will need to understand why this matters.

## Act Three: Implementation (Claude Code CLI)

Now comes the build. I switch to Claude Code—the terminal tool for agentic coding.

This is where most "AI built my app!" stories fall apart. Because reality hits you in the face.

### Problem 1: LangChain Import Hell

```python
from langchain.schema import Document
ModuleNotFoundError: No module named 'langchain.schema'
```

Fuck. LangChain restructured their packages.

**Me:** "Fix it."

**Claude:** *Updates imports to `langchain_core.documents`, adds `langchain-text-splitters` to requirements*

Five minutes. Solved.

### Problem 2: ChromaDB Type Validation

```python
ValueError: Expected metadata value to be a str, int, float, bool, 
got 2025-06-15 which is a date
```

YAML is parsing dates as Python date objects. ChromaDB only accepts primitives.

**Me:** "Fix the metadata conversion."

**Claude:** *Adds type conversion logic—dates to strings, lists to comma-separated strings*

Another five minutes.

### Problem 3: Progress Indicator Conflicts

The indexing takes 5-10 minutes. I'm going to sleep. I need progress bars so I know it's not hung.

We add `tqdm` for progress bars, `caffeinate` to prevent Mac sleep, comprehensive logging to `logs/`.

When I wake up, if it crashed, I have stack traces. If it worked, I have timestamps showing how long each step took.

This is engineering. This is the unsexy work that makes tools actually usable.

## The Build Session: 303 Episodes, 37,450 Chunks

```bash
./setup.sh
```

**Output:**
```
📚 Loading transcripts: 303/303 [00:00<00:00, 984 episodes/s]
✂️  Chunking: 303/303 [00:00<00:00, 416 episodes/s]
🧠 Creating embeddings... (~5-10 minutes)
✅ Indexed 37,450 chunks from 303 episodes
```

It worked.

## The Test

```bash
python explore.py 'What does Lenny say about pricing?'
```

**Output:**
```
💡 Answer:
--------------------------------------------------
Based on the context provided, Lenny recognizes pricing as 
worthy of deep discussion. He asks guests about common mistakes, 
biggest opportunities missed, and different strategic approaches...
--------------------------------------------------

📚 Sources:
• Todd Jackson: "A framework for finding product-market fit" (2024-04-11)
  https://www.youtube.com/watch?v=yc1Uwhfxacs
• Naomi Ionita: "How to price your product" (2023-01-12)
  https://www.youtube.com/watch?v=xvQadImf568

ℹ️  Cost: ~$0.0014
```

Source attribution. YouTube links. Publication dates. Cost transparency.

This isn't a demo. This is a *tool*.

## The Real Costs (Because We're Product Managers)

Let's talk actual numbers. Not estimates. Measured API usage.

**5 test queries (from API logs):**
- Input tokens: 4,258
- Output tokens: 893
- Total cost: **$0.007** (seven-tenths of a penny)
- Per query: **$0.0014** (about 1/7th of a penny)

**Development costs:**
- This conversation (architecture + debugging): ~$0.15 using Claude Sonnet 4
- Setup embeddings: $0.00 (runs locally)
- **Total project cost: ~$0.16** (sixteen cents)

**Extrapolated usage:**
- 100 queries/month: $0.14
- 1,000 queries/month: $1.40
- 10,000 queries/month: $14.00

Compare to ChatGPT Plus ($20/month flat rate) or Claude Pro ($20/month). If you're running thousands of queries, this is way cheaper.

The cost transparency isn't just nice—it's strategic. When you know exactly what each query costs, you can make rational decisions about model switching (v0.5) or adding more expensive features.

## What I Learned About PM-AI Collaboration

### 1. Progressive Elaboration Works

- **Phone:** High-level concept, validate approach
- **Desktop:** Architecture decisions, documentation
- **CLI:** Implementation, debugging, shipping

Each tool has a role. Don't try to code on your phone. Don't try to brainstorm in the terminal.

### 2. Strategic Decisions Are Still Yours

Claude suggested technologies. I chose them based on my constraints:
- No vendor lock-in → ChromaDB over Pinecone
- No recurring costs → Local embeddings over OpenAI
- Mac-first → Windows in v3.0, not v0.1

AI accelerates research. It doesn't replace judgment.

### 3. Discipline Beats Features

We could have built model switching in v0.1. We could have added Jupyter notebooks. We could have made it cross-platform.

Instead, we shipped ONE thing: queries work.

Now users have a tool. In v0.5, they'll get model switching. In v1.0, Jupyter.

This is how you ship fast: by shipping *less*.

### 4. Documentation Is Part of the Product

We created:
- README with clear setup instructions
- CLAUDE.md with architectural decisions
- CONTRIBUTING.md with contribution guidelines
- GitHub issue templates
- LICENSE file
- Release notes

Why? Because a tool without docs is a puzzle. And PMs don't want puzzles—they want answers.

Claude helped draft these, but I shaped them. Voice matters. Clarity matters.

## The Meta Lesson

This isn't a story about AI replacing developers.

This is a story about a PM with:
- Clear product vision (query Lenny's corpus)
- Technical knowledge (enough to make architectural calls)
- Discipline (one feature per version)
- AI tooling (to accelerate the grunt work)

...who shipped a working tool in one night.

Could I have done this without Claude? Yes, but it would have taken a weekend, not a night. I would have spent hours reading LangChain docs, debugging ChromaDB type errors, and writing boilerplate.

Claude compressed that from hours to minutes.

## What's Next

**v0.5 - Model Switching**

Add `--model` flag. Support Claude Sonnet 4, GPT-4.

One feature. Ships in a week.

**v0.75 - Web Search Fallback**

When RAG returns "I don't have information," trigger web search.

One feature. Ships in two weeks.

**v1.7 - Corpus Sync**

Script to pull new episodes from ChatPRD upstream, incremental re-indexing.

One feature. Ships when it's needed.

We'll get there. One feature at a time.

## Try It Yourself

The repo is public: [github.com/deanpeters/lennysan-rag-o-matic](https://github.com/deanpeters/lennysan-rag-o-matic)

Clone it. Run `./setup.sh`. Ask questions.

If you find bugs, open an issue. If you want features, check the roadmap first—we ship one at a time.

And if you're a PM thinking "I could never build this"—yes, you could.

You just need:
1. A clear vision
2. Enough technical knowledge to make calls
3. Discipline to ship one feature at a time
4. AI tools to handle the grunt work

That's it. That's the new PM superpower.

## The Uncomfortable Truth

We're not replacing engineers. We're changing what PMs can do before handing work to engineers.

Used to be: PM writes spec → Engineer implements → PM validates

Now it's: PM builds v0.1 proof of life → PM validates with users → PM hands to engineer with working prototype

The spec isn't a document anymore. It's a working CLI tool with logs, tests, and documentation.

This makes engineering handoffs clearer, faster, and less prone to miscommunication.

Engineers should welcome this. They get fewer "build me a thing and we'll see if users want it" projects. They get more "here's a validated prototype, make it production-ready" projects.

That's a better use of everyone's time.

## One More Thing

At 3 AM, lying in bed with my phone, I had an idea.

By morning, I had architecture.

By night, I had a shipped v0.1.

That's the PM workflow now.

Get comfortable with it.

---

*Dean Peters is Principal Consultant at Productside, teaching AI product management to enterprise clients. He writes about AI product management without the hype at [substack link]. This tool? It's open source. Go use it.*

---

## Appendix: The Tools

**Hardware:**
- iPhone (conceptual phase)
- MacBook Pro (architecture + implementation)

**AI Tools:**
- Claude (Anthropic) - mobile app, desktop app, Claude Code CLI
- All conversations in one thread, context preserved across devices

**Development Stack:**
- Python 3.13
- ChromaDB (vector database)
- LangChain (RAG framework)
- sentence-transformers (embeddings)
- Claude Haiku 4.5 (LLM)

**Time Investment:**
- Concept: 30 minutes (phone, in bed)
- Architecture: 2 hours (desktop, morning coffee)
- Implementation: 4 hours (CLI, debugging, docs)
- **Total: One night**

**Actual Cost (Measured):**
- Setup: $0.00 (local embeddings, no API calls)
- Per query: $0.0014 (measured across 5 test queries)
- 5 test queries: $0.007 total (less than a penny)
- Development session: ~$0.15 (Claude Sonnet 4 for architecture/debugging via Desktop/Code)
- **Total project cost: $0.157** (sixteen cents)

**Lines of Code:**
- Python: ~600 lines
- Bash: ~200 lines
- Documentation: ~2,000 words

**Result:**
- 303 episodes indexed
- 37,450 chunks searchable
- Full metadata preserved
- Source attribution on every query
- Comprehensive logging
- Complete documentation
- MIT licensed
- Ready for contributors

**Not bad for a night's work.**
