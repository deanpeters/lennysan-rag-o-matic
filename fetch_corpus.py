#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v1.0 — Corpus Fetcher
Fetches transcripts and metadata directly from YouTube.
No YouTube API key required — uses yt-dlp + youtube-transcript-api.

Usage:
    python fetch_corpus.py              # fetch new episodes only
    python fetch_corpus.py --full       # re-fetch all episodes (ignores sync state)
    python fetch_corpus.py --dry-run    # show what would be fetched, don't write

After fetching, re-index with:
    python index_corpus.py
"""

import os
import re
import sys
import json
import copy
import yaml
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# ── Optional: keyword generation via Haiku ────────────────────────────────────
try:
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    HAIKU_AVAILABLE = True
except ImportError:
    HAIKU_AVAILABLE = False

# ── Optional: youtube-transcript-api ─────────────────────────────────────────
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "pipeline": {
        "channel_url": "https://www.youtube.com/@LennysPodcast",
        "episodes_dir": "episodes",
        "sync_state_file": ".sync_state",
        "auto_index_after_fetch": False,
        "generate_keywords": True,
        "keyword_model": "claude-haiku-4-5-20251001",
        "max_episodes": None,  # None = no limit
        "whisper_fallback": False,  # future: use Whisper if captions unavailable
    }
}


def load_config(path: str = "CONFIGS.yaml") -> dict:
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        if "pipeline" in user_config:
            config["pipeline"].update(user_config["pipeline"])
    except Exception:
        pass
    return config


def load_sync_state(path: str) -> dict:
    if not os.path.exists(path):
        return {"fetched_video_ids": [], "last_fetch": None, "episode_count": 0}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"fetched_video_ids": [], "last_fetch": None, "episode_count": 0}


def save_sync_state(path: str, state: dict):
    state["last_fetch"] = datetime.now().strftime("%Y-%m-%d")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── YouTube fetching via yt-dlp ───────────────────────────────────────────────

def check_yt_dlp() -> bool:
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


MIN_EPISODE_DURATION = 300  # seconds — filter out Shorts and clips (< 5 min)


def fetch_channel_videos(channel_url: str, max_episodes: int = None) -> list[dict]:
    """
    Use yt-dlp to list all videos from a channel without downloading audio.
    Returns a list of dicts with video metadata, excluding Shorts and clips.
    Uses tab-separated output to avoid conflicts with | in episode titles.
    """
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s\t%(title)s\t%(upload_date)s\t%(duration)s\t%(view_count)s",
        "--no-warnings",
        "--quiet",
    ]
    cmd.append(channel_url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        print("❌ yt-dlp timed out fetching the channel. Check your connection.")
        return []

    if result.returncode != 0:
        print(f"❌ yt-dlp error: {result.stderr.strip()}")
        return []

    all_videos = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t", 4)
        if len(parts) < 4:
            continue
        video_id = parts[0].strip()
        title = parts[1].strip()
        upload_date = parts[2].strip()
        duration_raw = parts[3].strip()
        view_count_raw = parts[4].strip() if len(parts) > 4 else "0"

        # Filter out Shorts and clips — full episodes are > MIN_EPISODE_DURATION
        try:
            duration_seconds = float(duration_raw)
        except (ValueError, TypeError):
            continue  # NA or missing duration = Short/clip, skip it
        if duration_seconds < MIN_EPISODE_DURATION:
            continue

        h = int(duration_seconds // 3600)
        m = int((duration_seconds % 3600) // 60)
        s = int(duration_seconds % 60)
        duration_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

        try:
            publish_date = datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            publish_date = ""

        try:
            view_count = int(view_count_raw)
        except (ValueError, TypeError):
            view_count = 0

        all_videos.append({
            "video_id": video_id,
            "title": title,
            "publish_date": publish_date,
            "duration_seconds": duration_seconds,
            "duration": duration_str,
            "view_count": view_count,
            "description": "",  # fetched separately for new episodes only
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            "channel": "Lenny's Podcast",
        })

    # Apply limit after filtering Shorts
    if max_episodes:
        all_videos = all_videos[:max_episodes]

    return all_videos


def fetch_video_description(video_id: str) -> str:
    """Fetch full description for a single video (only called for new episodes)."""
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--print", "%(description)s",
        "--no-warnings",
        "--quiet",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


# ── Guest name extraction ─────────────────────────────────────────────────────

def extract_guest(title: str) -> str:
    """
    Parse guest name from Lenny's episode title.
    Common patterns:
      "Pricing strategies | Jason Lemkin"
      "How Notion grew | Ivan Zhao, CEO of Notion"
      "Head of Claude Code: What happens after coding | Boris Cherny"
      "Sequoia CEO Coach on leadership | Brian Halligan"
      "Jenny Wen (head of design at Claude)"
      "Brian Chesky's big ambitions for Airbnb"
    """
    if " | " in title:
        after_pipe = title.rsplit(" | ", 1)[-1].strip()

        # Strip parenthetical role: "Jenny Wen (head of design at Claude)" → "Jenny Wen"
        after_pipe = re.sub(r"\s*\([^)]+\)", "", after_pipe).strip()

        # Strip after comma: "Ivan Zhao, CEO of Notion" → "Ivan Zhao"
        after_pipe = re.split(r",\s+", after_pipe)[0].strip()

        # Strip leading role/org words before the actual name.
        # "Sequoia CEO Coach Brian Halligan" → "Brian Halligan"
        # Strategy: take the last two words, which are almost always "First Last".
        # Handles prefixes like "Dr." by accepting 3-word results when first word is a title.
        words = after_pipe.split()
        if len(words) >= 3 and re.match(r"^(Dr|Mr|Ms|Mrs|Prof)\.?$", words[-3], re.IGNORECASE):
            return " ".join(words[-3:])
        if len(words) >= 2:
            return " ".join(words[-2:])
        return after_pipe

    # Pattern: "Name's [topic]" — possessive at the start
    possessive = re.match(r"^([A-Z][a-z]+ [A-Z][a-z]+)'s\b", title)
    if possessive:
        return possessive.group(1)

    # Pattern: "First Last on [topic]"
    on_pattern = re.match(r"^([A-Z][a-z]+ [A-Z][a-z]+) on\b", title)
    if on_pattern:
        return on_pattern.group(1)

    # No guest identifiable — solo/Lenny episode
    return "unknown"


def guest_to_slug(guest: str, title: str = "") -> str:
    if guest == "unknown" and title:
        # Use title-based slug so solo episodes don't collide
        slug = title.lower()
        slug = re.sub(r"\s*\([^)]+\)", "", slug)   # strip parentheticals
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        return slug.strip("-")[:60] or "unknown"
    slug = guest.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "unknown"


# ── Transcript fetching ───────────────────────────────────────────────────────

def fetch_transcript(video_id: str) -> tuple[str, str]:
    """
    Returns (transcript_text, method_used).
    Tries youtube-transcript-api first.
    Returns ("", "unavailable") if nothing works.
    """
    if TRANSCRIPT_API_AVAILABLE:
        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id)
            text = " ".join(s.text for s in transcript)
            return text, "youtube-captions"
        except Exception:
            pass

    # Future: Whisper fallback goes here (v1.x)
    return "", "unavailable"


# ── Keyword generation (optional, requires Anthropic key) ────────────────────

def generate_keywords(title: str, description: str, model_id: str) -> list[str]:
    if not HAIKU_AVAILABLE:
        return []
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return []
    try:
        llm = ChatAnthropic(model=model_id, temperature=0)
        template = """Generate 5-8 short keyword tags for this podcast episode.
Return only lowercase hyphenated keywords, one per line. No bullets, no numbers.
Examples: product-strategy, pricing, growth, leadership, hiring

Title: {title}
Description: {description}

Keywords:"""
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"title": title, "description": description[:500]})
        keywords = [
            re.sub(r"[^a-z0-9-]", "", line.strip().lower().replace(" ", "-"))
            for line in result.strip().splitlines()
            if line.strip()
        ]
        return [k for k in keywords if k][:8]
    except Exception:
        return []


# ── Write transcript.md ───────────────────────────────────────────────────────

def write_episode(episodes_dir: str, video: dict, guest: str, slug: str,
                  transcript: str, keywords: list[str], dry_run: bool) -> bool:
    episode_dir = Path(episodes_dir) / slug
    transcript_path = episode_dir / "transcript.md"

    if dry_run:
        print(f"    → Would write: {transcript_path}")
        return True

    episode_dir.mkdir(parents=True, exist_ok=True)

    # Build YAML frontmatter
    frontmatter = {
        "guest": guest,
        "title": video["title"],
        "youtube_url": video["youtube_url"],
        "video_id": video["video_id"],
        "publish_date": video["publish_date"],
        "description": video["description"],
        "duration_seconds": video["duration_seconds"],
        "duration": video["duration"],
        "view_count": video["view_count"],
        "channel": video["channel"],
        "keywords": keywords or [],
    }

    yaml_str = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)

    content = f"---\n{yaml_str}---\n\n# {video['title']}\n\n## Transcript\n\n{transcript}\n"

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch Lenny's podcast transcripts from YouTube",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Re-fetch all episodes (ignores sync state)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fetched without writing any files",
    )
    parser.add_argument(
        "--no-keywords",
        action="store_true",
        help="Skip keyword generation (faster, no Anthropic API call)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only fetch the N most recent episodes (useful for testing)",
    )
    args = parser.parse_args()

    config = load_config()
    pipeline = config["pipeline"]

    channel_url = pipeline.get("channel_url", "https://www.youtube.com/@LennysPodcast")
    episodes_dir = pipeline.get("episodes_dir", "episodes")
    sync_state_file = pipeline.get("sync_state_file", ".sync_state")
    auto_index = pipeline.get("auto_index_after_fetch", False)
    generate_kw = pipeline.get("generate_keywords", True) and not args.no_keywords
    keyword_model = pipeline.get("keyword_model", "claude-haiku-4-5-20251001")
    max_episodes = args.limit or pipeline.get("max_episodes")

    print()
    print("🎙️  LennySan RAG-o-Matic — Corpus Fetcher")
    print("=" * 50)

    # Preflight
    if not check_yt_dlp():
        print("❌ yt-dlp not found.")
        print()
        print("Install it:")
        print("  pip install yt-dlp")
        print("  or: brew install yt-dlp")
        return 1

    if not TRANSCRIPT_API_AVAILABLE:
        print("❌ youtube-transcript-api not found.")
        print()
        print("Install it:")
        print("  pip install youtube-transcript-api")
        return 1

    if args.dry_run:
        print("🔍 DRY RUN — no files will be written")
        print()

    # Load sync state
    state = load_sync_state(sync_state_file)
    known_ids = set(state.get("fetched_video_ids", []))

    if args.full:
        print("🔄 Full re-fetch mode — ignoring sync state")
        known_ids = set()

    # Also check which episodes already exist on disk
    existing_slugs = set()
    if Path(episodes_dir).exists():
        existing_slugs = {p.parent.name for p in Path(episodes_dir).glob("*/transcript.md")}

    print(f"📡 Fetching video list from: {channel_url}")
    if max_episodes:
        print(f"   (limited to {max_episodes} most recent)")
    print()

    videos = fetch_channel_videos(channel_url, max_episodes)
    if not videos:
        print("❌ No videos found. Check the channel URL in CONFIGS.yaml.")
        return 1

    print(f"📋 Found {len(videos)} videos on channel")

    # Filter to new ones
    new_videos = [v for v in videos if v["video_id"] not in known_ids]
    if not args.full:
        print(f"✅ {len(videos) - len(new_videos)} already fetched")
        print(f"🆕 {len(new_videos)} new episode(s) to fetch")
    print()

    if not new_videos:
        print("Nothing new to fetch. Corpus is up to date.")
        print()
        return 0

    # Fetch each new episode
    fetched = 0
    skipped = 0
    failed = 0

    for i, video in enumerate(new_videos, 1):
        title = video["title"]
        video_id = video["video_id"]
        guest = extract_guest(title)
        slug = guest_to_slug(guest, title)

        # Make slug unique if collision
        candidate_slug = slug
        counter = 2
        while candidate_slug in existing_slugs and not args.full:
            candidate_slug = f"{slug}-{counter}"
            counter += 1
        slug = candidate_slug

        print(f"[{i}/{len(new_videos)}] {title}")
        print(f"    Guest: {guest}  |  Slug: {slug}")

        # Fetch description (skipped in dry-run to save time)
        if not args.dry_run:
            video["description"] = fetch_video_description(video["video_id"])

        # Fetch transcript
        transcript, method = fetch_transcript(video_id)
        if not transcript:
            print(f"    ⚠️  No transcript available — skipping")
            skipped += 1
            continue
        print(f"    📄 Transcript: {method} ({len(transcript.split())} words)")

        # Generate keywords
        keywords = []
        if generate_kw:
            keywords = generate_keywords(title, video.get("description", ""), keyword_model)
            if keywords:
                print(f"    🏷️  Keywords: {', '.join(keywords)}")

        # Write episode
        write_episode(episodes_dir, video, guest, slug, transcript, keywords, args.dry_run)

        if not args.dry_run:
            existing_slugs.add(slug)
            known_ids.add(video_id)
            state["fetched_video_ids"] = list(known_ids)
            state["episode_count"] = len(existing_slugs)
            save_sync_state(sync_state_file, state)

        fetched += 1
        print()

    # Summary
    print("=" * 50)
    print(f"✅ Fetched: {fetched}  |  Skipped (no captions): {skipped}  |  Failed: {failed}")
    print()

    if fetched > 0 and not args.dry_run:
        if auto_index:
            print("🔄 Auto-indexing enabled — running index_corpus.py...")
            print()
            subprocess.run([sys.executable, "index_corpus.py"])
        else:
            print("Next step: re-index to pick up new episodes:")
            print("  python index_corpus.py")
            print()

    return 0


if __name__ == "__main__":
    exit(main())
