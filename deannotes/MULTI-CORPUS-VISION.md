# Multi-Corpus Vision — Design Doc

## The Idea

Two distinct expert knowledge bases. One synthesis layer.

- **Lenny corpus** — practitioners sharing it live. Founders, PMs, and operators in
  conversation with Lenny, working through hard-won lessons from building real products.
- **Productside corpus** — practitioners who've done it and are now teaching it.
  Experienced PMs and product leaders turning field experience into structured curriculum.

Each corpus stays sovereign. You can query either one alone. But the real power
is querying both and letting Dean-i-fried blend the practitioner voice with the
educator voice into a single, punchy synthesis.

**The question no tool answers today:**
"What does the practitioner evidence say, what does the framework evidence say,
and what's the Deanified collision between the two?"

---

## What Each Corpus Brings

| | Lenny Corpus | Productside Corpus |
|---|---|---|
| Source | Lenny's Podcast (YouTube) | Productside webinars (YouTube) |
| Voice | Practitioner in conversation — messy, specific, earned | Practitioner-turned-teacher — structured, transferable, field-tested |
| Content | Guest stories, decisions, war stories | Frameworks, models, PM skill-building grounded in real experience |
| Slug style | Guest-based (`brian-chesky/`) | Topic-based (`discovery-frameworks/`) |
| Metadata | Guest, title, date, YouTube URL | Topic, speaker, date, YouTube URL |

---

## User Experience

### Single corpus query (unchanged from today)
```bash
python explore.py "What does Lenny say about pricing?"
```
```bash
python explore.py --corpus productside "What does Productside say about pricing?"
```

### Cross-corpus query (new)
```bash
python explore.py --corpus all "How should PMs think about pricing?"
```

Returns:
- **From Lenny's corpus** — Direct answer + Related insights
- **From Productside corpus** — Direct answer + Related insights
- **Dean-i-fried synthesis** — one punchy take that collides both perspectives

### Browser UI
Corpus selector in the sidebar:
- Lenny's Podcast
- Productside
- Both (enables cross-corpus Dean-i-fried)

---

## Architecture Sketch

### Storage
Each corpus gets its own ChromaDB collection:
```
data/
  chroma_db/
    lenny/          ← existing collection
    productside/    ← new collection
```

### Config
```yaml
corpora:
  lenny:
    type: youtube_channel
    channel_id: "UC..."
    slug_field: guest
    chroma_collection: lenny
    label: "Lenny's Podcast"

  productside:
    type: youtube_channel
    channel_id: "UC..."
    slug_field: topic
    chroma_collection: productside
    label: "Productside"
```

### Pipeline (shared, parameterized)
One `index_corpus.py` that reads corpus config and builds the right collection.
One `fetch_transcripts.py` that pulls from YouTube Data API + youtube-transcript-api,
assembles YAML frontmatter, and writes episode files into the right directory.

### Query layer
- Single corpus: query one collection, return structured answer
- Both corpora: query each collection independently, get two structured answers,
  pass both to Dean-i-fried for cross-corpus synthesis

---

## Dean-i-fried Cross-Corpus Synthesis

The synthesis prompt gets four inputs instead of two:

```
Lenny Direct answer: ...
Lenny Indirect insights: ...
Productside Direct answer: ...
Productside Indirect insights: ...
```

The voice rules stay the same. The synthesis task gets richer:
find the collision, the contradiction, or the unexpected harmony between
practitioner evidence and educator framework. That's where the value lives.

---

## The Pipeline (YouTube → YAML frontmatter → ChromaDB)

Replaces dependency on ChatPRD/lennys-podcast-transcripts for Lenny,
and enables any YouTube-based corpus to be added via config.

### Steps
1. **YouTube Data API** — list all videos from channel, get metadata
   (title, description, publish date, video_id, duration, view_count)
2. **youtube-transcript-api** — pull auto-captions for each video
3. **Guest/topic extraction** — parse from title (heuristic + Haiku fallback)
4. **Keyword generation** — Haiku call on description + transcript sample
5. **Write transcript.md** — same YAML frontmatter format as existing corpus
6. **Incremental** — skip episodes already present, only process new ones

### New dependencies
- `google-api-python-client` — YouTube Data API v3 (free, 10k units/day)
- `youtube-transcript-api` — auto-captions (no API key needed)

### Honest tradeoffs vs ChatPRD upstream
- ✅ No dependency on external maintainer
- ✅ New episodes available immediately
- ✅ Works for any YouTube channel
- ⚠️ YouTube auto-captions — good quality, no speaker attribution
- ⚠️ Guest name extraction needs heuristics (titles vary)
- ⚠️ More moving parts than `git fetch upstream`

---

## Roadmap Fit

This collapses and supersedes several roadmap items:

| Old item | New status |
|---|---|
| v1.7: Corpus Sync | Replaced by YouTube pipeline (more powerful) |
| v2.5: Second Corpus | This is it, with Productside as the concrete target |

**Suggested phasing:**
- **v1.7** — YouTube pipeline for Lenny (self-contained, no ChatPRD dependency)
- **v2.5** — Productside corpus + cross-corpus query + Dean-i-fried synthesis

---

## Open Questions (Decide Before Building)

1. **Productside YouTube channel ID** — need the actual channel to confirm
   transcript availability and volume.
2. **Slug field for Productside** — topic-based or speaker-based?
3. **Cross-corpus Dean-i-fried** — one combined synthesis, or show each corpus
   answer separately first and then synthesize? (Recommend: show both, then synth.)
4. **Browser UI corpus selector** — dropdown or checkboxes?
   (Recommend: radio with "Both" as an option.)
5. **Index management** — one `index_corpus.py` run per corpus, or one run for all?
6. **Lenny corpus transition** — keep existing ChatPRD-sourced episodes and
   supplement with YouTube pipeline, or full rebuild?
   (Recommend: supplement first, full rebuild optional.)

---

## Why This Matters

Most RAG tools are single-source lookup engines.
This becomes a **comparative knowledge platform** — practitioner in conversation
vs practitioner-turned-teacher, story vs structured model, earned lesson vs
taught framework. Both sides have done the work. The difference is the lens.

Dean-i-fried is the synthesis that no one else has.
Not because the technology is novel, but because the collision is deliberate.

Optional. Explicit. Grounded in two corpuses. Deanified into one.
