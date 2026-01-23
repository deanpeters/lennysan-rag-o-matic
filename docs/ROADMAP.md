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

- **v0.85: Dean-i-fried response mode (optional)**  
  **What:** Add an optional “Dean-i-fried” synthesis that blends direct + inferred answers into the Dean voice.  
  **Why you care:** You get a punchier, more memorable synthesis when you want it, without losing the grounded answer.

- **v0.86: Lenny Therapy mode (facilitated reflection)**  
  **What:** Add an optional “Lenny Therapy” mode that reframes retrieved insights into facilitator-style questions using MI/CBT-inspired techniques, grounded in transcript evidence (direct + inferred).  
  **Why you care:** Instead of only getting answers dumped on you, the system can help you think more clearly about stressful PM situations by reflecting, reframing, and asking better questions.

- **v0.9: `explore.py` diagnostic logs**  
  **What:** Save what happened during a run: settings, retrieval, decisions, errors.  
  **Why you care:** Debugging stops being séance work. You can explain behavior, reproduce issues, and learn faster.

- **v1.0: Jupyter support (one example notebook)**  
  **What:** The first notebook that shows “query -> evidence -> synthesis” with analysis steps.  
  **Why you care:** This is where the repo turns into a personal research lab, not just a CLI tool.

- **v1.35: Brevity vs verbose mode**  
  **What:** A response length mode to trade clarity vs cost, with explicit tuning for short or detailed answers.  
  **Why you care:** You can dial down token spend on quick checks, or dial up detail when you are deep in research.

- **v1.5: Topic organization**  
  **What:** Better structure for themes, tags, and curated paths.  
  **Why you care:** You’ll stop re-discovering the same episodes and start building repeatable learning journeys.

- **v1.6: Substack mode (Dean voice output)**  
  **What:** A Substack‑ready output mode that blends RAG evidence with Dean‑style narrative learned from his Substack writing.  
  **Why you care:** It turns raw insight into publishable, data‑infused writing without copy‑paste gymnastics.

- **v1.7: Corpus sync**  
  **What:** Keep transcripts and metadata updated without manual churn.  
  **Why you care:** Your tool doesn’t rot. New episodes show up without you doing weekend chores.

- **v2.0: Streamlit UI**  
  **What:** A simple UI for browsing, querying, and inspecting sources.  
  **Why you care:** Easier demos, easier teaching, easier “look, here’s the receipts” sharing.

- **v2.5: Second corpus**  
  **What:** Add another transcript set (or your own) alongside Lenny’s.  
  **Why you care:** You can compare perspectives across sources and build your own research stack.

- **v3.0: Windows support**  
  **What:** Works for teams that don’t live on Macs.  
  **Why you care:** This stops being “Dean’s fun toy” and becomes team-adoptable.

- **v4.0: Local LLMs**  
  **What:** Run models locally, reduce reliance on APIs.  
  **Why you care:** Privacy, cost control, and offline experimentation when you need it.
