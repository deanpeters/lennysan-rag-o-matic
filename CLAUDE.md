# CLAUDE.md - Builder Instructions for LennySan RAG-o-Matic

## Project Vision

LennySan RAG-o-Matic is a low-barrier PM research tool that lets product managers explore Lenny Rachitsky's podcast corpus using AI and RAG. The philosophy: **we get more done faster by focusing on less**. Each version adds ONE capability.

## Core Principles

1. **Vertical slices**: Each version ships one focused feature
2. **Low barrier**: Non-technical PMs should be able to fork, clone, and run
3. **Transparent costs**: Users understand what they're spending on API calls
4. **No vendor lock-in**: Architecture supports multiple LLM providers
5. **Mac-first, then expand**: v0.1-2.5 Mac only, v3.0 adds Windows

## Current Status: v0.1 (Proof of Life)

**What exists:**
- ✅ CLI query tool (`explore.py`)
- ✅ Indexing script (`index_corpus.py`) with YAML metadata preservation
- ✅ Setup automation (`setup.sh`)
- ✅ ChromaDB for vector storage with metadata
- ✅ Claude Haiku integration (cheapest model)
- ✅ Source attribution (guest, title, date, YouTube links)
- ✅ Mac-only support

**What's explicitly NOT in v0.1:**
- ❌ Model switching (that's v0.5)
- ❌ Jupyter notebooks (that's v1.0)
- ❌ Topic organization (that's v1.5)
- ❌ Multiple corpuses (that's v2.5)

## Architecture Decisions (v0.1)

### Why ChromaDB?
- Runs locally (no cloud account needed)
- Free and open source
- Simple setup for non-technical users
- Persistent storage without separate server

### Why Claude Haiku?
- Cheapest model (~$0.001-0.005 per query)
- Good enough for proof of life
- Tests the full pipeline without spending money
- Users can upgrade to better models in v0.5+

### Why sentence-transformers/all-MiniLM-L6-v2?
- Free local embeddings (no API costs)
- Fast enough for 320 episodes
- Good quality for semantic search
- No external dependencies

### Why LangChain?
- Abstracts RAG complexity
- Makes model switching easy (v0.5)
- Well-documented for PM audience
- Industry standard (teaching value)

### Why Preserve YAML Metadata?
**Critical architectural decision**: Claire Vo enriched each transcript with YAML frontmatter containing:
- Guest name and episode title
- Publication date (YYYY-MM-DD format)
- Keywords (topic tags like "pricing", "growth", "leadership")
- Duration, view count, and YouTube URL

**Our approach:**
1. Parse YAML frontmatter separately from transcript content
2. Attach metadata to each text chunk during indexing
3. ChromaDB stores both content vectors AND metadata
4. Retrieval returns chunks with full metadata intact
5. `explore.py` formats sources with attribution

**Why this matters:**
- **Trust**: Users see which episode/guest provided the answer
- **Context**: Publication date matters (advice from 2020 vs 2024)
- **Deep dive**: YouTube links let users hear the full context
- **Future filtering** (v0.5+): Query "Brian Chesky on pricing" or "recent episodes about AI"
- **Quality signal**: View count and keywords indicate episode relevance

**Implementation details:**
- Uses PyYAML to parse frontmatter
- Each Document object carries metadata dict
- Text splitting preserves metadata on every chunk
- LangChain's RetrievalQA returns source_documents
- Custom formatting in `explore.py` deduplicates and displays top 3 sources

**Do NOT remove this in future versions** - metadata preservation is foundational to the project's value proposition.

## v0.1 Implementation Details

### What setup.sh Does
1. **Preflight checks**: Verifies Mac OS, Git, Python 3.9+, ANTHROPIC_API_KEY
2. **Directory creation**: Creates `data/chroma_db/` for vector storage
3. **Virtual environment**: Sets up isolated Python environment in `.venv/`
4. **Dependencies**: Installs packages from `requirements.txt`
5. **Indexing**: Runs `index_corpus.py` to process the existing `episodes/` directory

**Important**: The `episodes/` directory is already present from the fork - setup.sh does NOT clone it. It processes what's already there.

### What index_corpus.py Does
1. **Scans episodes/**: Finds all `*/transcript.md` files
2. **Parses YAML**: Splits frontmatter from content using PyYAML
3. **Creates Documents**: Each transcript becomes a LangChain Document with metadata
4. **Chunks text**: Splits into 1000-char chunks with 200-char overlap
5. **Preserves metadata**: Every chunk carries the full episode metadata
6. **Generates embeddings**: Uses sentence-transformers locally (no API cost)
7. **Stores in ChromaDB**: Persists to `data/chroma_db/` with metadata

### What explore.py Does
1. **Validates environment**: Checks for API key and vector database
2. **Loads vectorstore**: Connects to existing ChromaDB
3. **Queries**: Converts natural language to vector search
4. **Retrieves chunks**: Gets top 5 relevant chunks with metadata
5. **Synthesizes answer**: Uses Claude Haiku to generate response
6. **Formats sources**: Deduplicates episodes, shows top 3 with guest/title/date/URL

### File Paths (Accurate as of v0.1)
- **Source transcripts**: `/episodes/{guest-name}/transcript.md` (from fork)
- **Vector database**: `/data/chroma_db/` (generated, gitignored)
- **Virtual environment**: `/.venv/` (generated, gitignored)
- **Python files**: `/index_corpus.py`, `/explore.py`, `/setup.sh` (in repo)
- **Config**: `/requirements.txt`, `/.gitignore` (in repo)
- **Docs**: `/README.md`, `/CLAUDE.md`, `/GITLENNY.md` (in repo)

### Cost Breakdown (v0.1)
- **Embeddings**: $0 (local model, no API calls)
- **Indexing**: One-time, ~5-10 minutes compute time
- **Per query**: ~$0.001-0.005 (Claude Haiku API)
- **Storage**: ~500MB local disk for ChromaDB

**Total setup cost**: $0 for embeddings + first query costs pennies

## Directory Structure

```
lennysan-rag-o-matic/
├── episodes/               # Lenny's transcripts (from fork)
│   └── {guest-name}/
│       └── transcript.md   # YAML frontmatter + content
├── data/                   # Generated (gitignored)
│   └── chroma_db/         # Vector database
├── .venv/                 # Python virtual env (gitignored)
├── explore.py             # CLI tool
├── index_corpus.py        # Indexing script
├── setup.sh              # Setup automation
├── requirements.txt       # Python dependencies
├── README.md             # User-facing documentation
├── CLAUDE.md             # This file - builder instructions
├── GITLENNY.md           # Fork/sync instructions
└── .gitignore
```

## Roadmap (One Feature Per Version)

**v0.1 - Proof of Life** ✅ Current
- CLI works with Claude Haiku
- Single feature: basic RAG query loop

**v0.5 - Model Switching**
- Add `--model` flag to explore.py
- Support: claude-haiku, claude-sonnet-4, gpt-4
- Single feature: choose your model

**v0.75 - Web Search Fallback** (New!)
- Add `--web-fallback` flag
- If RAG returns "I don't have information...", trigger web search
- Combine corpus insights with current web info
- Single feature: handle queries outside corpus scope

**v1.0 - Jupyter Support**
- Add Jupyter to requirements.txt
- Create one example notebook
- Single feature: interactive exploration

**v1.5 - Topic Organization**
- Create topics/ directory structure
- Add 3-4 example notebooks (pricing, growth, AI, enterprise)
- Single feature: organized research

**v1.7 - Corpus Sync**
- Create `sync_corpus.sh` script
- Check ChatPRD upstream for new episodes since last sync
- Only re-index new episodes (incremental)
- Track sync state in `.sync_state` file
- Single feature: stay current with new episodes

**v2.0 - Streamlit UI**
- Add streamlit to requirements.txt
- Create basic web interface
- Single feature: visual queries

**v2.5 - Second Corpus**
- Refactor to support multiple corpuses/
- Add one more source (Productside or community choice)
- Single feature: compare across sources

**v3.0 - Windows Support**
- Create setup.bat
- Cross-platform testing
- Single feature: works on Windows

**v4.0 - Local LLMs** (Major release)
- Integrate LlamaFarm
- Support Ollama models
- Single feature: fully offline operation

## Building Future Versions

### For v0.5 (Model Switching)

The groundwork is already there. You need to:

1. Update `explore.py`:
   - Add argparse for `--model` flag
   - Create model mapping dict
   - Support both Anthropic and OpenAI
   - Default to claude-sonnet-4 (better than Haiku, cheaper than 4.5)

2. Update `requirements.txt`:
   - Add `openai>=1.0.0`
   - Add `langchain-openai>=0.0.5`

3. Update error handling:
   - Check for appropriate API keys based on model choice
   - Graceful fallback if key missing

4. Update README:
   - Document new `--model` flag
   - Show cost comparison per model
   - Update "Current Status" to v0.5

**Do NOT add:**
- Config files (keep it simple)
- Multiple file changes
- Jupyter support (that's v1.0)

### For v1.0 (Jupyter)

1. Add to `requirements.txt`:
   - `jupyter>=1.0.0`
   - `ipykernel>=6.0.0`

2. Create `notebooks/` directory:
   - Create `example_exploration.ipynb`
   - Show: load vectorstore, run query, display results
   - Keep it minimal (one notebook)

3. Update setup.sh:
   - Register kernel: `python -m ipykernel install --user --name=lennysan`

4. Update README:
   - Add Jupyter quick start
   - Link to example notebook
   - Update "Current Status" to v1.0

**Do NOT add:**
- Multiple notebooks (that's v1.5)
- Topic organization (that's v1.5)
- Fancy visualizations

### For v1.7 (Corpus Sync)

**The Problem**: New Lenny episodes get added to ChatPRD repo regularly. Users need an easy way to stay current.

**The Solution**: Create `sync_corpus.sh` script that:

1. **Fetches upstream changes**:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Detects new episodes**:
   - Compare current episode count vs last sync
   - List new transcript files
   - Store sync state in `.sync_state` (gitignored)

3. **Incremental indexing**:
   - Only process new episodes (not entire corpus)
   - Use ChromaDB's `add_documents()` method
   - Append to existing vector store

4. **Usage**:
   ```bash
   ./sync_corpus.sh
   # Output: "Found 3 new episodes. Re-indexing... Done!"
   ```

**Do NOT add:**
- Cron automation (let users decide when to sync)
- Complex state management (keep it simple)
- Auto-sync on query (too expensive)

**Key insight**: Incremental indexing is WAY faster than full re-index (~30 seconds vs 5-10 minutes).

### For v2.1 (Google Colab)

1. Create `colab_setup.ipynb` notebook
2. Handle Colab-specific quirks:
   - No persistent storage (mount Google Drive)
   - No local file system (clone repo in Colab)
   - API keys via Colab secrets
3. Test on free Colab tier
4. Update README with Colab badge

**Do NOT add:**
- Pro/Pro+ specific features
- GPU requirements (CPU embeddings are fine)

### For v2.6 (Obsidian Export)

1. Add `--export-obsidian` flag to explore.py
2. After query, write to `~/Documents/Obsidian/LennyRAG/`:
   - File per query: `YYYY-MM-DD-query-slug.md`
   - Include: question, answer, sources with wiki-links
   - Format: Obsidian markdown (wiki-links, tags)
3. Detect Obsidian vault location (configurable)

**Do NOT add:**
- Notion export (that's different)
- Bi-directional sync (overkill)
- Obsidian plugin (separate project)

### General Guidelines for All Versions

**When building new features:**
1. Read this CLAUDE.md first
2. Check current version in README
3. Implement ONLY the single feature for that version
4. Update README "Current Status" section
5. Test the single feature
6. Update roadmap if needed

**File creation rules:**
- All new files go in the repo (no dynamic generation)
- Update .gitignore for any generated files
- Keep setup.sh simple (just orchestration)

**Testing strategy:**
- Test on Mac first (v0.1-2.5 requirement)
- Use Claude Haiku for development (cheap)
- Upgrade to better models for final testing

**Code style:**
- Clear error messages (PMs are the audience)
- Fail fast with helpful instructions
- Progress indicators for slow operations
- Cost information where relevant

## Common Pitfalls to Avoid

1. **Scope creep**: Don't add "just one more thing"
2. **Over-engineering**: PMs need simple, not clever
3. **Poor error messages**: "Error" is not helpful, "Run: export API_KEY='...'" is
4. **Silent failures**: Always print what went wrong
5. **Hidden costs**: Always tell users what API calls cost
6. **Mac-specific commands on Windows**: Check OS first (v3.0+)

## Extension Points (For Community)

**Where to add new features:**
- New models: Update explore.py model mapping
- New corpuses: Add to corpuses/ directory
- New topics: Add to topics/ directory (v1.5+)
- New interfaces: Add alongside explore.py (v2.0+)

**What to preserve:**
- Single-feature versions
- Low barrier to entry
- Clear cost information
- Simple setup process

## Testing Checklist (Before Shipping)

For any version:
- [ ] Fresh clone works on Mac
- [ ] setup.sh completes without errors
- [ ] New feature works as documented
- [ ] Error messages are helpful
- [ ] README reflects current state
- [ ] No scope creep beyond single feature
- [ ] Costs are transparent to user
- [ ] .gitignore excludes generated files

## Support Philosophy

This is a weekend project that teaches practical AI/RAG to PMs. Support is:
- Community-driven via GitHub issues
- Documentation-first (README, error messages)
- No hand-holding (PMs should learn by doing)
- Contributors welcome (clear contribution guidelines)

## Credits

Always maintain in README:
- Lenny Rachitsky (content creator)
- Claire Vo (transcript corpus creator)
- Link to original ChatPRD repo

## Final Reminder

**We get more done faster by focusing on less.**

If you're building a version and wondering "should I also add...?" - the answer is NO. Ship the single feature. Move to next version.
