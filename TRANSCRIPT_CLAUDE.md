# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a static content archive containing 303 episode transcripts from Lenny's Podcast, with an AI-generated topic index for easy discovery.

## Structure

```
├── episodes/
│   └── {guest-name}/
│       └── transcript.md    # YAML frontmatter + transcript content
├── index/
│   ├── README.md            # Main entry point with topic links
│   └── {topic}.md           # Individual topic files (e.g., product-management.md)
└── scripts/
    └── build-index.sh       # Script to regenerate the topic index
```

## Transcript Format

Each transcript.md contains:
- **YAML frontmatter**: guest, title, youtube_url, video_id, publish_date, description, duration_seconds, duration, view_count, channel, keywords
- **Transcript content**: Timestamped speaker dialogue

The `publish_date` field is in YYYY-MM-DD format and represents the YouTube upload date.

## Index

The `index/` folder contains AI-generated keyword tags for each episode:
- Topic files (e.g., `product-management.md`) - Episodes grouped by topic keyword

## Working with Large Transcript Files

Transcript files are large (often 25,000+ tokens). Use these strategies:

### 1. Use Grep for targeted searches (preferred)
```
# Search for specific topics across all transcripts
Grep pattern="product.market fit" path="episodes/"

# Search with context lines for better understanding
Grep pattern="early stage" path="episodes/" output_mode="content" -C=5
```

### 2. Read frontmatter first (lines 1-15)
Get metadata before deciding to read more:
```
Read file_path="episodes/guest-name/transcript.md" limit=15
```

### 3. Read in chunks when needed
For sequential reading, use offset/limit:
```
Read file_path="..." offset=1 limit=500    # First chunk
Read file_path="..." offset=500 limit=500  # Second chunk
```

### 4. Use Task tool with Explore agent
For research across multiple transcripts:
```
Task subagent_type="Explore" prompt="Find insights about X across transcripts"
```

### 5. Handle persisted output
When Read returns a persisted output path like:
`Output saved to: ~/.claude/.../tool-results/xxx.txt`
Read that file to access the full content.

## Rebuilding the Index

```bash
./scripts/build-index.sh
```

This calls Claude CLI for each episode to generate keywords. The script is idempotent - it skips episodes already present in keyword files, so it can be run multiple times safely.

## Adding Publication Dates

All episodes should include `publish_date` in ISO 8601 format (YYYY-MM-DD). To fetch the publication date for a new episode:

1. Use the `video_id` from the transcript's frontmatter
2. Call the YouTube Data API v3:
   ```
   https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}
   ```
3. Extract `snippet.publishedAt` from the response
4. Add `publish_date: YYYY-MM-DD` to the frontmatter after `video_id`
