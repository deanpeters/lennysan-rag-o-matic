# v0.1 - Proof of Life 🎉

**Release Date:** January 17, 2026  
**Status:** Mac-only, CLI-only, Claude Haiku only

First working version! Query 303 Lenny podcast episodes from your terminal with AI-powered answers and source attribution.

## What's New

### ✅ Core Features
- **CLI Query Tool**: Ask natural language questions via `explore.py`
- **Quick Activation**: `source activate.sh` to start exploring
- **Full Corpus Indexed**: 303 episodes → 37,450 searchable chunks
- **Metadata Preservation**: Every answer shows guest, title, date, keywords, YouTube link
- **Source Attribution**: See exactly which episodes informed the answer
- **Comprehensive Logging**: Debug with timestamped logs in `logs/`
- **Clean Output**: Suppressed deprecation warnings for better UX

### 🔧 Technical Stack
- **Vector DB**: ChromaDB (local, no cloud account)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (free, local)
- **LLM**: Claude Haiku 4.5 (cheapest for testing)
- **Framework**: LangChain with LCEL
- **Platform**: Mac only (v0.1)

### 💰 Cost Breakdown
- **Setup**: One-time, 5-10 minutes, ~$0 (local embeddings)
- **Per Query**: ~$0.001-0.005 (Claude Haiku)
- **Storage**: ~500MB local disk

## Example Queries

```bash
# Quick start (after setup)
cd ~/Code/lennysan-rag-o-matic
source activate.sh

# Run queries
python explore.py 'What does Lenny say about pricing?'
python explore.py 'How do you find product-market fit?'
python explore.py 'What are common mistakes in enterprise sales?'

# Exit when done
deactivate
```

## Example Output

```
🔍 Searching Lenny's podcast corpus...
❓ Question: What does Lenny say about pricing?

🤔 Thinking...

💡 Answer:
--------------------------------------------------
Based on the context provided, here's what Lenny says about pricing:

1. **Pricing deserves dedicated focus**: Lenny mentions that pricing 
   could warrant "a whole podcast on its own"...
--------------------------------------------------

📚 Sources:
• Todd Jackson: "A framework for finding product-market fit" (2024-04-11)
  https://www.youtube.com/watch?v=yc1Uwhfxacs
• Naomi Ionita: "How to price your product" (2023-01-12)
  https://www.youtube.com/watch?v=xvQadImf568

ℹ️  Using Claude Haiku (v0.1 proof of life)
   Cost: ~$0.001-0.005 per query
```

## Installation

See [README.md](README.md) for full setup instructions. TL;DR:

```bash
# Clone repo
git clone https://github.com/YOUR-USERNAME/lennysan-rag-o-matic
cd lennysan-rag-o-matic

# Set API key
export ANTHROPIC_API_KEY='sk-ant-...'

# Run setup (one time, 5-10 minutes)
chmod +x setup.sh
./setup.sh

# Query away!
python explore.py "your question here"
```

## What This Is NOT (Yet)

- ❌ Not model switching (coming in v0.5)
- ❌ Not web search fallback (coming in v0.75)
- ❌ Not Jupyter notebooks (coming in v1.0)
- ❌ Not topic organization (coming in v1.5)
- ❌ Not corpus sync (coming in v1.7)
- ❌ Not Streamlit UI (coming in v2.0)
- ❌ Not Google Colab (coming in v2.1)
- ❌ Not multi-corpus (coming in v2.5)
- ❌ Not Obsidian export (coming in v2.6)
- ❌ Not Windows compatible (coming in v3.0)
- ❌ Not local LLMs (coming in v4.0)

This is a **proof of life** - weekend build to validate the concept works.

## Known Issues

### Expected Limitations
- Mac only (Windows support in v3.0)
- Claude Haiku only (model switching in v0.5)
- CLI only (Streamlit UI in v2.0, Jupyter in v1.0)
- No web search fallback (v0.75)
- Corpus is static (sync script in v1.7)

### Rough Edges (Won't Fix in v0.1)
- Deprecation warnings suppressed but still in code
- No error recovery for partial indexing failures
- No query history
- No caching of repeated queries

## Bug Fixes from v0.01

- ✅ Fixed LangChain import errors (`langchain-core`, `langchain-text-splitters`)
- ✅ Fixed ChromaDB metadata type errors (dates converted to strings)
- ✅ Fixed progress bar kwargs conflict (removed duplicate `show_progress_bar`)
- ✅ Added proper error logging with stack traces
- ✅ Suppressed deprecation warnings for cleaner output

## Documentation

### New Files
- `LICENSE` - MIT license
- `CONTRIBUTING.md` - Contribution guidelines
- `CLAUDE.md` - Builder instructions for future versions
- `.github/ISSUE_TEMPLATE/` - Bug reports, feature requests, questions

### Updated Files
- `README.md` - Complete setup guide, roadmap through v4.0
- `.gitignore` - Protected logs, data, venv, API keys
- `requirements.txt` - All dependencies with versions

## Credits

### Built On
- **Transcript Corpus**: [ChatPRD/lennys-podcast-transcripts](https://github.com/ChatPRD/lennys-podcast-transcripts)
- **Metadata Enrichment**: Claire Vo (@clairevo on GitHub)
- **Podcast Host**: Lenny Rachitsky

### Technology Stack
- ChromaDB for vector storage
- sentence-transformers for embeddings
- LangChain for RAG orchestration
- Anthropic Claude for synthesis

## What's Next

### v0.5 - Model Switching (Next Release)
- Add `--model` flag to explore.py
- Support: claude-haiku, claude-sonnet-4, gpt-4
- One feature: choose your model

### v0.75 - Web Search Fallback
- Add `--web-fallback` flag
- If RAG returns "I don't have information...", trigger web search
- One feature: handle queries outside corpus scope

See [README.md](README.md#roadmap) for full roadmap through v4.0.

## Support

- 🐛 **Bug reports**: Use [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml)
- 💡 **Feature requests**: Use [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml)
- ❓ **Questions**: Use [Question template](.github/ISSUE_TEMPLATE/question.yml)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR-USERNAME/lennysan-rag-o-matic/discussions)

## Philosophy

**"We get more done faster by focusing on less."**

Each version ships ONE feature. No scope creep. No bundling. Just steady, disciplined progress.

---

**Enjoy querying Lenny's corpus! 🚀**

*Built by PMs, for PMs.*
