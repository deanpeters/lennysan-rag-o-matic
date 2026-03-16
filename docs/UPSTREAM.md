# Upstream Transcripts (Where the Corpus Comes From)

This repo is built on top of the **ChatPRD/lennys-podcast-transcripts** corpus. We treat that repo as the upstream source of truth for episode transcripts and metadata.

## What “upstream” means here

- **Upstream source:** `https://github.com/ChatPRD/lennys-podcast-transcripts`
- **Local fork:** `/Users/deanpeters/Code/lennys-podcast-transcripts`
- **This repo:** `/Users/deanpeters/Code/lennysan-rag-o-matic`

The RAG tool does **not** auto‑pull transcripts. You only get new episodes when you **manually sync** and merge them into this repo.

## How updates flow into this repo

When you sync properly (see `GITLENNY.md`):

- ✅ New episodes arrive in `episodes/`
- ✅ Upstream README/CLAUDE snapshots update into:
  - `TRANSCRIPT_README.md`
  - `TRANSCRIPT_CLAUDE.md`
- ✅ `index/` updates (if upstream changed them)
- ❌ Your `README.md` and `CLAUDE.md` are **protected** (not overwritten)

## Quick sync (safe, protective merge)

Run this inside `lennysan-rag-o-matic`:

```bash
git fetch upstream

git merge upstream/main --no-commit --no-ff

# Keep our custom docs

git checkout --ours README.md CLAUDE.md

# Refresh upstream snapshots

git show upstream/main:README.md > TRANSCRIPT_README.md

git show upstream/main:CLAUDE.md > TRANSCRIPT_CLAUDE.md

# Stage and commit

git add TRANSCRIPT_README.md TRANSCRIPT_CLAUDE.md README.md CLAUDE.md

git commit -m "sync: merge upstream transcripts (preserve custom docs)"
```

## Why this protects your README

Upstream changes do not overwrite your README unless you let them. The key line is:

```
git checkout --ours README.md CLAUDE.md
```

That explicitly keeps **your** README and CLAUDE while still pulling new episodes
and refreshing `TRANSCRIPT_README.md` / `TRANSCRIPT_CLAUDE.md`.

## Safety rails (so we never nuke this repo again)

These steps prevent accidental pushes from the transcripts repo into this repo:

1) **Never push from the transcripts repo to a redirected remote.**
   If GitHub says “this repository moved,” STOP. That means your push is being
   redirected somewhere else (like this repo). Do not force-push.

2) **Use fetch-only upstream.**
   In `lennysan-rag-o-matic`, set upstream to fetch-only so you can’t push by mistake:

   ```
   git remote set-url --push upstream DISABLE
   ```

3) **Verify remotes before force-pushing.**
   Always check:

   ```
   git remote -v
   ```

   Make sure you are in the right repo, and the push URL matches the repo you intend.

## Are we up to date right now?

Only if you ran the sync steps above **inside this repo**. Updating the upstream fork
alone does **not** update this repo.

If you want to verify, compare the top of `TRANSCRIPT_README.md` to the upstream
README and check the latest episode dates in `episodes/`.
