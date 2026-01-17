# AGENTS.md — Working Agreements for LennySan RAG-o-Matic
This file is based on CLAUDE.md, for use by Codex and similar tools.

## Purpose
Build and evolve a low-barrier PM research tool that lets product managers explore Lenny Rachitsky’s podcast corpus using RAG. Philosophy: ship ONE capability per version.

## Non-Negotiables
- Preserve YAML frontmatter metadata end-to-end (parse → chunk → store → retrieve → display).
- Never remove or weaken source attribution (guest, title, date, URL).
- Keep setup and usage low-barrier for non-technical users.
- Track and communicate costs (embeddings + per-query LLM calls).
- Maintain a “one feature per version” scope discipline.

## Current Release Target
- Current: v0.5 (model switching)
- Next planned: v0.6 (CONFIGS.yaml)

## Golden Path Commands (v0.1)
- Setup + index:
  - `./setup.sh`
- Query:
  - `python explore.py "your question here"`

## Repo Map (v0.1)
- `setup.sh`
  - Preflight checks, creates `.venv`, installs deps, builds index into `data/chroma_db/`
- `index_corpus.py`
  - Parses `episodes/**/transcript.md`, extracts YAML frontmatter + content, chunks text, embeds locally, persists to ChromaDB
- `explore.py`
  - Loads ChromaDB, retrieves relevant chunks, calls the LLM to synthesize an answer, prints answer + deduped top sources
- Source transcripts:
  - `episodes/{guest-name}/transcript.md` (from upstream fork)
- Generated (gitignored):
  - `.venv/`
  - `data/chroma_db/`
  - `logs/` (if present)

## Critical Architectural Decision: YAML Metadata Preservation
Claire Vo enriched transcripts with YAML frontmatter containing:
- guest name, episode title
- publication date (YYYY-MM-DD)
- keywords (topic tags)
- duration, view count, YouTube URL

Implementation requirements:
- Parse YAML frontmatter separately from transcript content (PyYAML).
- Attach the metadata dict to every chunk produced during indexing.
- Persist both embeddings and metadata in ChromaDB.
- Retrieval must return source documents with metadata intact.
- `explore.py` must format sources using metadata and dedupe by episode.
- Always show attribution for the top sources (at least the top 3).

Do not remove or bypass this system. It is foundational to trust, context, and deep-dive workflows.

## Technical Choices (v0.5) — Keep Unless Upgrading Deliberately
- Vector store: ChromaDB (local)
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (local/free)
- LLMs: Claude Haiku / Claude Sonnet 4 / GPT‑4o mini / GPT‑4o (via --model)
- Orchestration: LangChain + LCEL (enables later provider switching)

## Cost Expectations (v0.1)
- Embeddings/indexing: $0 API spend (local embeddings)
- Indexing: one-time local compute (minutes)
- Per query: low-cost LLM call (order of thousandths of a dollar)
- Disk: local ChromaDB size can be hundreds of MB

## Change Rules
When changing anything, follow these rules:
- If you change chunking parameters, document the change and bump/index-version strategy as needed.
- If you change output formatting, keep source attribution intact and stable.
- If you add flags/options, update README usage examples.
- Avoid adding multiple major capabilities in one version.

## Validation Checklist (before committing)
- `./setup.sh` works on a clean Mac environment (Python 3.9+).
- Index build completes and persists to `data/chroma_db/`.
- `python explore.py "test query"` returns:
  - a coherent answer
  - at least one source with guest/title/date/URL
- No generated artifacts are committed (vector DB, venv, logs, `.env`).

## Roadmap Guardrails (One Feature Per Version)
- v0.5: model switching via a `--model` flag (Haiku/Sonnet/GPT-4 as applicable)
- v0.6: CONFIGS.yaml for centralized defaults/paths
- v0.75: optional web fallback via a `--web-fallback` flag (only when corpus lacks info)
- v1.0: Jupyter notebook support (one example notebook)
- v1.5: topic organization (structured notebooks/topics)
- v1.7: corpus sync (incremental re-index of new episodes)
- v2.0: Streamlit UI
- v2.5: second corpus support
- v3.0: Windows support
