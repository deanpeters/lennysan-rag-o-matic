# LennySan RAG-o-Matic

```
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
                                                       v0.6
```
                                                       
A low-barrier, learn-by-building PM pm research tool for exploring Lenny Rachitsky's 320+ podcast episodes using AI and RAG from the CLI, with future support for Jupyter notebooks, time-series exploration, and more.

## What This Does

Stop rebuilding Claude Projects or Gemini Gems every time you want to explore a PM topic. Clone this once, run it locally, and query Lenny's entire podcast corpus with your choice of LLM.

**Use cases:**
- Research pricing strategies across 50+ episodes
- Compare AI product management perspectives
- Extract frameworks for enterprise sales
- Find real-world examples for specific PM challenges
- Build topic-specific notebooks for your own learning

No cloud accounts, no recurring costs beyond LLM API calls (typically pennies per query).

## Behind the Scenes

**Want to see how this was built?** Check out [`deannotes/SESSION.0.1.STORY.md`](deannotes/SESSION.0.1.STORY.md) - the complete narrative of building v0.1 in 3 hours 40 minutes (1 AM to 4:40 AM). Includes:
- Real problems and solutions (LangChain hell, ChromaDB types, progress bars)
- PM instincts in action (security, debugging, UX, cost transparency)
- Actual measured costs ($0.16 + 20% of weekly Claude Pro limits)
- Why metadata preservation matters
- The brutal truth about platform limits

More articles coming as we ship each version.

## Who This Is For

Product managers comfortable with:
- Forking and cloning GitHub repos
- Setting environment variables
- Running command-line tools

If you're not there yet, use Claude Projects or ChatGPT Custom GPTs instead. No shame - different tools for different comfort levels.

## Current Status: v0.6 (CONFIGS.yaml)

**What works right now:**
- CLI query tool
- Lenny corpus indexed in ChromaDB
- Model switching across Anthropic + OpenAI
- `--list-models` helper to see available choices
- CONFIGS.yaml for editable defaults (models, paths, retrieval)
- Mac only

**Release notes:**
- `releasenotes/RELEASE_v0.62.md`
- `releasenotes/RELEASE_v0.6.md`
- `releasenotes/RELEASE_v0.5.md`
- `releasenotes/RELEASE_v0.1.md`

**What this is NOT yet:**
- Not Jupyter notebooks (v1.0)
- Not topic organization (v1.5)
- Not Streamlit UI (v2.0)
- Not multiple corpuses (v2.5)
- Not Windows compatible (v3.0)
- Not local LLMs (v4.0)

This is a weekend build to prove the RAG concept works. Expect rough edges.

## How It Works

LennySan RAG-o-Matic consists of three key components that work together:

### 1. **setup.sh** - One-Command Setup
Your entry point. Runs preflight checks, creates a Python virtual environment, installs dependencies, and orchestrates the indexing process. Run it once, then you're ready to explore.

### 2. **index_corpus.py** - Smart Indexing
Processes all 320 episodes and their rich metadata into a searchable vector database. Here's what makes it special:

**Preserves Claire Vo's Metadata**: Each transcript includes YAML frontmatter with:
- Guest name and episode title
- Publication date
- Keywords (pricing, growth, leadership, etc.)
- Duration, view count, and YouTube links

Rather than treating this as plain text, we parse and preserve it. This means every chunk in the database knows which episode it came from, who the guest was, when it was published, and what topics it covers.

**Why this matters**: You don't just get an answer—you get attribution. Know which episode, guest, and date the insights came from. This builds trust and lets you dig deeper.

### 3. **explore.py** - CLI Query Tool
Your research interface. Ask questions in natural language, get AI-synthesized answers from the corpus, with full source attribution showing guest, title, date, and YouTube link.

Example output:
```
💡 Answer:
Lenny discusses several pricing strategies including value-based pricing...

📚 Sources:
• Madhavan Ramanujam: "The 1 thing that most gets in the way..." (2023-05-15)
  https://www.youtube.com/watch?v=xyz
```

**The RAG Pipeline**: Your query → Vector search finds relevant chunks → Model synthesizes an answer (direct + inferred + missing) → You get insights with sources.

### Bonus: Topic Index (Inherited from Original Repo)

The fork includes an `index/` directory with 80+ topic files (`pricing.md`, `growth-strategy.md`, etc.) containing AI-generated episode tags. This is a **complementary resource** to the RAG system:

- **RAG system** (our addition): Ask natural language questions, get synthesized answers
- **Topic index** (from original repo): Browse episodes by keyword tag

Use both! The topic files are great for discovering episodes, while the RAG system is great for extracting insights across episodes.

## Prerequisites

**Required for v0.6:**
- GitHub account (you're here, so ✓)
- [Anthropic API key](https://console.anthropic.com/) (for Claude models)
- [OpenAI API key](https://platform.openai.com/) (for GPT models)
- Python 3.9 or higher
- Git

**Recommended:**
- **Mac**: [Homebrew](https://brew.sh) for managing dependencies

## Getting Started

### Forking and Cloning

This project is a fork of the [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts) repository. If you want to create your own fork and keep it synced with updates, see [GITLENNY.md](GITLENNY.md) for detailed instructions.

**Quick start (use this fork as-is):**

1. **Clone this repo:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/lennysan-rag-o-matic
   cd lennysan-rag-o-matic
   ```

2. **Set your Anthropic API key (required for Claude models):**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export ANTHROPIC_API_KEY='sk-ant-...'

   # Reload your shell
   source ~/.bashrc  # or source ~/.zshrc
   ```

3. **(Optional) Set your OpenAI API key (only if using GPT models):**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export OPENAI_API_KEY='sk-...'

   # Reload your shell
   source ~/.bashrc  # or source ~/.zshrc
   ```

4. **Run setup:**
   ```bash
   chmod +x setup.sh activate.sh  # Make scripts executable
   ./setup.sh
   ```
   This will:
   - Check prerequisites
   - Install Python dependencies
   - Index transcripts in ChromaDB (one-time, ~5-10 minutes)

5. **Ask a question:**
   ```bash
   # Activate environment (first time)
   source .venv/bin/activate
   
   # Or use the convenience script (after first time)
   source activate.sh
   
   # Query away (default model: Claude Haiku)
   python explore.py "What does Lenny say about pricing?"

   # Choose a model
   python explore.py --model sonnet-4 "What does Lenny say about pricing?"
   python explore.py --model gpt-4o-mini "What does Lenny say about pricing?"
   python explore.py "What does Lenny say about pricing?" --model gpt-4o

   # List available models
   python explore.py --list-models
   
   # Exit when done
   deactivate
   ```

That's it. You now have 320 episodes searchable from your command line.

## Configuration (v0.6)

`CONFIGS.yaml` lets non‑technical PMs safely change defaults without touching code.
CLI flags always win, so power users can override config when needed.

```yaml
defaults:
  model: "haiku"  # haiku | sonnet-4 | gpt-4o-mini | gpt-4o

paths:
  vector_db: "data/chroma_db"

retrieval:
  search_type: "mmr"
  k: 8
  fetch_k: 24
```

Edit `CONFIGS.yaml` in the repo root. If the file is missing, the tool uses built‑in defaults.

## Cost Expectations (v0.6)

**Actual measured costs (Haiku baseline):**
- **Setup**: $0 (local embeddings, no API calls)
- **Per query**: $0.0014 (measured from 5 test queries)
- **Local storage**: ~500MB

**Example usage:**
- 100 queries: $0.14
- 1,000 queries: $1.40
- Compare to ChatGPT Plus ($20/month) or Claude Pro ($20/month)

**Model cost tiers (rule of thumb):**

| Model | Cost | When to use |
| --- | --- | --- |
| `haiku` | Cheapest | Smoke tests, quick checks |
| `gpt-4o-mini` | Very cheap | OpenAI smoke tests |
| `sonnet-4` | Mid | Deeper analysis |
| `gpt-4o` | Mid‑high | OpenAI quality runs |

Use Haiku or GPT‑4o mini for cheap smoke tests, and Sonnet 4 or GPT‑4o for higher‑quality answers.

## Tactical Roadmap

Each version adds ONE focused capability. We ship fast by staying narrow.

**v0.01 - Get Started**
- Inspired by Lenny Rachitsky with grattitude
- Facilitated by Clari Vo's generosity
- Git the repo (SEE GITLENNY.md) & rename
- publish deanpeters/lennysan-rag-o-matic

**v0.1 - Proof of Life** ✅ Shipped
- CLI works with Claude Haiku
- Proof the RAG loop works end‑to‑end

**v0.5 - Model Switching** ✅ Shipped
- Add `--model` flag
- Support Claude Haiku, Claude Sonnet 4, GPT‑4o mini, GPT‑4o
- One feature: choose your model

**v0.6 - CONFIGS.yaml** ✅ Current
- Add a single configuration file for defaults and paths
- Keep CLI flags as overrides (no breaking changes)
- One feature: centralize configuration

**v0.75 - Web Search Fallback**
- Add `--web-fallback` flag
- If corpus lacks info, search the web
- One feature: handle out-of-scope queries

**v1.0 - Jupyter Support**
- Jupyter notebooks work
- One example notebook included
- One feature: interactive exploration

**v1.5 - Topic Organization**
- Topic directory structure
- 3-4 example topic notebooks (pricing, growth, AI, enterprise)
- One feature: organized research

**v1.7 - Corpus Sync**
- Inspired by Clair Vo's awesome ChatPRD/lennys-podcast-transcripts repo
- Script to sync with ChatPRD upstream repo
- Detect new episodes since last sync
- Incremental re-indexing (only new content)
- One feature: stay up-to-date with new episodes

**v2.0 - Streamlit UI**
- Inspired by Kenny at Productside
- Basic web interface
- Point-and-click queries
- One feature: visual interface

**v2.1 - Google Colab Support**
- Inspired by a Productside Webinar
- Colab-compatible setup notebook
- No local installation needed
- One feature: run in browser

**v2.5 - Second Corpus**
- Multi-corpus architecture
- Add one more source (Productside or community choice)
- One feature: compare across sources

**v2.6 - Obsidian Export**
- Inspired by a recent Teresa Torres podcast
- Export findings to Obsidian markdown format
- Preserve links and metadata
- One feature: integrate with personal knowledge base

**v3.0 - Windows Support**
- Cross-platform setup.bat
- Windows testing
- One feature: works everywhere

**v4.0 - Local LLMs** (Major release)
- LlamaFarm integration
- Fully offline operation
- One feature: no API costs

## What Gets Set Up (v0.6)
```
lennysan-rag-o-matic/
├── CONFIGS.yaml           # Defaults for models, paths, retrieval
├── episodes/               # Lenny's transcripts (already here)
├── deannotes/              # Dean's articles and build stories
│   ├── README.md          # Article index
│   └── SESSION.0.1.STORY.md  # How v0.1 was built (1 AM - 4:40 AM)
├── data/
│   └── chroma_db/         # Your local vector database (created by setup)
├── logs/                  # Setup and indexing logs (created by setup)
├── explore.py             # CLI tool
├── index_corpus.py        # Indexing script
├── setup.sh              # Setup script
├── activate.sh           # Quick activation helper
├── requirements.txt       # Python dependencies
└── README.md
```

More structure added in later versions.

## Troubleshooting

**"No ANTHROPIC_API_KEY found"**
- Check if it's set: `printenv ANTHROPIC_API_KEY > /dev/null && echo "✅ It exists" || echo "❌ Not set"`
- Add to your shell profile (`~/.bashrc` or `~/.zshrc`):
  ```bash
  export ANTHROPIC_API_KEY='sk-ant-...'
  ```
- Reload shell: `source ~/.bashrc` or `source ~/.zshrc`
- Or just edit `~/.zshrc` directly and restart terminal

**Model Switching (v0.5)**
- List available models: `python explore.py --list-models`
- If you pick a GPT model, set `OPENAI_API_KEY` (Claude models use `ANTHROPIC_API_KEY`)
- If you see a key error, re-source your shell: `source ~/.zshrc`
- Start with cheap models for smoke tests: `--model haiku` or `--model gpt-4o-mini`
- If answers feel too strict, the CLI now uses a 3‑section response to separate direct vs inferred insights.

**"Command not found: python"**
- Try `python3` instead
- Or install Python 3.9+ from python.org

**"Setup fails on dependencies"**
- Make sure you're using Python 3.9 or higher: `python3 --version`
- Try: `pip install --upgrade pip` then rerun setup

**"Permission denied: ./setup.sh"**
- Make it executable: `chmod +x setup.sh`

**"Setup failed but I don't know why"**
- Check the logs: `logs/setup_YYYYMMDD_HHMMSS.log`
- Check the indexing logs: `logs/index_YYYYMMDD_HHMMSS.log`
- Logs contain full error details and stack traces

**Something else broken?**
- Open an issue with your error message
- Include OS version and Python version

## Credits

- **Lenny Rachitsky** for 320+ episodes of PM wisdom
- **Claire Vo** ([@clairevo](https://twitter.com/clairevo)) for creating and open-sourcing the transcript corpus, including the rich YAML metadata (guest, title, date, keywords) that makes smart attribution possible
- Original transcript repo: [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts)

## License

MIT License - same as the source transcript corpus. Fork it, extend it, learn from it.

## Contributing

**v0.6 contributions welcome:**
- Bug fixes
- Better error messages
- Mac compatibility improvements

**Future versions seeking help:**
- v0.75+: Web search fallback behavior and guardrails
- v1.0+: Jupyter notebook examples
- v2.5+: Additional corpus sources
- v3.0: Windows setup.bat and testing

Open issues to discuss before submitting PRs. We ship one feature at a time.

## Support

This is a community tool built in spare time. No official support, but:
- Open issues for bugs
- Discussions for questions
- PRs for improvements

Built by PMs, for PMs. We get more done faster by focusing on less.
