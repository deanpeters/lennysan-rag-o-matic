# What's New in v0.9 — Browser UI

The CLI is still here. It's not going anywhere. But now there's a browser. `streamlit run app.py`, and you're querying Lenny's corpus from a tab like a person who owns nice things.

Full parity with the CLI: model switching, web search fallback, Dean-i-fried voice, full analysis vs. direct answer only. Everything controlled from a sidebar that doesn't require a man page to understand. Hover any option for a plain-English explanation. Open the "What do these mean?" expander for the full glossary without leaving the page.

New: **export to markdown**. Every answer gets a download button. One click, clean `.md` file with your question, answer, sources, and Dean-i-fried if you had it on. Named from your question so the filesystem stays sane.

The CLI isn't deprecated. It's the spine. The browser is for everyone else at the table.

## What changed

- `app.py` — new Streamlit browser UI
- `requirements.txt` — added `streamlit>=1.35.0`

## How to launch

```bash
source .venv/bin/activate
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501`.
