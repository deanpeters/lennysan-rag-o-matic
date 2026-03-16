# Roadmap (One Feature Per Version)

# Roadmap (Tactical, One Feature Per Version)

This is a **tactical roadmap**, not a strategy manifesto. It exists to keep this repo shippable, testable, and useful, version by version, without turning into a philosophical debate club.

At Productside we teach two truths that explain this file:
- “Strategy without tactics is the slowest route to victory, tactics without strategy is the noise before defeat.” ~ Sun Tzu
- “However beautiful the strategy, you should occasionally look at the results.” ~ Winston Churchill

This roadmap is the “look at the results” part. It’s the sequence of concrete moves that turn the strategy into working software.

## Overview

The rule is intentionally simple: **one meaningful capability per version**.

That rule gives you three wins:
- you can understand what changed without reading code
- you can test releases without building an entire QA department
- you can say “not yet” to shiny ideas without killing momentum

Use this file for:
- what’s next, and why it’s next
- what’s explicitly not happening (yet)
- how v0.x grows into v1.0 notebooks without chaos

---

Each version adds **ONE focused capability**. Not because we lack imagination, but because shipping one real thing beats dreaming about twelve. Or, in Productside Dean-isms:

- “Don’t boil the ocean.”
- “We get more done, faster, by focusing on less.”

Here’s the “what changed” plus the “why you, a PM, should care.”  
(✅ = released)

- ✅ **v0.1: Proof-of-life CLI RAG loop**  
  **What:** Ask a question, retrieve transcript chunks, get an answer with citations.  
  **Why you care:** This is the “receipts, not vibes” foundation. Everything else rides on it.

- ✅ **v0.5: Model switching (`--model`)**  
  **What:** Swap LLMs (Claude vs GPT families) without rewriting code.  
  **Why you care:** You can compare quality vs cost fast, and stop marrying one vendor like it’s 2012.

- ✅ **v0.6: `CONFIGS.yaml` defaults**  
  **What:** Centralized defaults for stable behavior.  
  **Why you care:** You get consistency. Your experiments become repeatable instead of “what flags did I use last time?”

- ✅ **v0.75: Web search fallback (AUTO + ALWAYS)**  
  **What:** Optional web search when the corpus can’t answer cleanly.  
  **Why you care:** You stop bouncing between tools. You can keep momentum when the transcripts hit a gap.

- ✅ **v0.8: Docker search option (one-button script)**  
  **What:** Run search locally via Docker instead of relying on an external API.  
  **Why you care:** More control, more privacy, and fewer “third party services own my query history” vibes.

- ✅ **v0.85: Dean-i-fried response mode (optional)**
  **What:** Add an optional “Dean-i-fried” synthesis that blends direct + inferred answers into the Dean voice.
  **Why you care:** You get a punchier, more memorable synthesis when you want it, without losing the grounded answer.

- ✅ **v0.9: Browser UI (Streamlit)**
  **What:** Query from your browser — full parity with the CLI, human-first UX, one-click Markdown export. Pulled forward from v2.0.
  **Why you care:** No terminal required after setup. Pick your model, ask your question, download the answer. Everyone at the table can use it.

- **v1.0: Self-contained corpus pipeline (own the transcripts)**
  **What:** Replace the ChatPRD upstream dependency with a direct YouTube pipeline. YouTube Data API for metadata + auto-captions for transcripts. Config-driven, incremental, works for any YouTube channel. Lenny stays Lenny — same format, same index, we just own the feed.
  **Why you care:** Keeping the corpus current in an era of disruptive innovation is paramount. You can’t build a reliable research tool on a corpus that might be weeks or months stale. This makes freshness a property of the tool, not a prayer to an upstream maintainer.

- **v1.2: Lenny Therapy mode (facilitated reflection)**
  **What:** An optional mode that reframes corpus evidence into facilitator-style questions grounded in transcript evidence — direct + inferred. Reflects, reframes, never prescribes. Design doc: `deannotes/LENNY-THERAPY.md`.
  **Why you care:** Sometimes you don’t need another answer. You need a better question. This mode slows the moment down and surfaces collective wisdom through a facilitator’s lens instead of an answer engine’s.

- **v1.4: Diagnostic logs**
  **What:** Save what happened during a run — settings, retrieval decisions, errors — to a `logs/` directory.
  **Why you care:** Debugging stops being séance work. You can explain behavior, reproduce issues, and learn faster.

- **v1.6: Topic organization**
  **What:** Curated paths through the corpus by theme — pricing, growth, hiring, AI, leadership. Each topic is a structured entry point into the most relevant episodes, not just a keyword search.
  **Why you care:** You stop re-discovering the same episodes and start building repeatable research journeys. Topics are the difference between a search engine and a curriculum.

- **v2.0: Productside corpus + cross-corpus Dean-i-fried**
  **What:** Add Productside as a second named corpus (experienced PMs coaching and teaching great product management). Query either corpus alone or both together. When querying both: each answers independently, then Dean-i-fried synthesizes the collision into one punchy take. Design doc: `deannotes/MULTI-CORPUS-VISION.md`.
  **Why you care:** Practitioners telling stories vs. experienced PMs coaching craft — that’s not the same angle twice. Dean-i-fried finds the collision between them and turns it into something no single-corpus tool can produce.

- **v2.5: Streamlit UI** *(pulled forward as v0.9)*
  **What:** Shipped early. See v0.9 above.

- **v3.0: Windows support**
  **What:** Works for teams that don’t live on Macs.
  **Why you care:** This stops being “Dean’s fun toy” and becomes team-adoptable.

- **v4.0: Local LLMs**
  **What:** Run models locally, reduce reliance on APIs.
  **Why you care:** Privacy, cost control, and offline experimentation when you need it.

---

### On the shelf (valid, lower urgency)

- **Jupyter support** — interactive exploration via notebooks
- **Topic organization** — curated paths by theme
- **Brevity vs verbose mode** — configurable answer length
- **Substack mode** — Dean voice output formatted for publishing
- **Corpus sync script** — simple git-based sync (superseded by v1.0 pipeline for most users)
