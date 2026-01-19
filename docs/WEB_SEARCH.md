# Web Search (API and Docker)

Sometimes the transcripts won’t have your answer. That’s not failure. That’s reality. Web search is the optional “break glass” feature for when the corpus can’t cover what you’re asking, or when you want a quick sanity check against the wider internet.

This doc exists because web search is powerful and also dangerous in the boring ways: cost creep, slower runs, and answers that get less traceable if you don’t keep a tight leash. The goal here is to help you use it intentionally, not accidentally.

If you want the full CLI command buffet (models, verbosity, flag order, output style), that lives in:
- [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md)

## Overview

Web search is **off by default**. You enable it when you want it.

Web search is optional and controlled. It only runs when:
- you pass `--web-search on|always`, or
- `CONFIGS.yaml` says it should

You have two choices for providers:
- **API provider**: simplest setup, fastest to start, may cost money
- **Docker provider**: runs locally, more control, more moving parts

You also have two usage modes:
- **AUTO**: only use search when retrieval looks weak
- **ALWAYS**: force web search every time (use sparingly)

The rule of thumb:
- If you’re learning the corpus, keep web search off.
- If you’re stuck, enable it, run the query again, then inspect the sources like a grownup.

---

## Quick examples (the only ones most humans need)

### Turn web search on and try again

~~~bash
python explore.py --web-search on "Why does SAFe suck?"
~~~

### Force web search every time (use sparingly)

~~~bash
python explore.py --web-search always "Why does SAFe suck?"
~~~

### Turn web search off (back to pure corpus mode)

~~~bash
python explore.py --web-search off "Why does SAFe suck?"
~~~

### Use Docker as the provider for one run

~~~bash
python explore.py --web-search always --web-provider docker "Why does SAFe suck?"
~~~

### Add diagnostics when something feels weird

~~~bash
python explore.py --web-search always --verbose on "Why does SAFe suck?"
~~~

---

## API search (default)

This is the easiest path. Lowest friction. The best “just keep going” option.

- Requires `SERPER_API_KEY`
- Fastest time-to-first-result
- Good enough for most cases

---

## Docker search (advanced)

Docker is powerful, but it can be fragile. Think of it like a box of puppies: free to adopt, but it may take more care than you expected.

If you want a one-button Docker experience (no config edits):

~~~bash
chmod +x scripts/docker_search.sh
./scripts/docker_search.sh "why safe sucks"
~~~

If port 8080 is taken:

~~~bash
SEARXNG_PORT=8081 ./scripts/docker_search.sh "why safe sucks"
~~~

You can also override the provider in the CLI:

~~~bash
python explore.py --web-search always --web-provider docker "why safe sucks"
~~~

## If Docker feels like too much

Switch back to API search and keep going. The goal is learning, not suffering.

## Diagnostics

Run with verbose:

~~~bash
python explore.py --web-search always --web-provider docker --verbose on "why safe sucks"
~~~

You will see a short diagnostic line after the answer if the web search failed.
