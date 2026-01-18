# GITLENNY.md

## How to Fork, Rename, and Sync "Lenny's Podcast Transcripts"

**Target Audience:** Non-programmers or anyone looking to build a custom tool on top of the original transcripts.

This guide covers two workflows for working with Lenny's transcripts:
- **Part 1: Initial Setup** - Fork and set up your repo (one-time)
- **Part 2: Staying in Sync** - Pull upstream updates (recurring)

---

## Part 1: Initial Setup (One-Time)

This section explains how to take the original transcript repository, create your own copy (fork) with a custom name, and keep it linked to the original so you can pull in new episodes as they are released.

### Prerequisites

1. **GitHub CLI installed:** Ensure you have the `gh` tool installed on your machine.
2. **Terminal:** Open your terminal (Mac/Linux) or command prompt.

---

### Step 1: Navigate to your code folder

Go to the folder where you keep your coding projects.

```bash
cd <path-to-your-code-folder>
# Example: cd /Users/myname/Code/

```

### Step 2: Fork the repository (without downloading yet)

We create a copy of the repository in your GitHub account, but we skip downloading (cloning) it immediately so we can rename it first.

```bash
gh repo fork ChatPRD/lennys-podcast-transcripts --clone=false

```

### Step 3: Rename your fork

Give your version of the repository a unique name (e.g., `lennys-rag-o-matic`).

```bash
gh repo rename <your-new-repo-name> --repo <your-github-username>/lennys-podcast-transcripts --yes

```

### Step 4: Clone (Download) your new repository

Now, download your renamed repository to your local machine.

```bash
gh repo clone <your-github-username>/<your-new-repo-name> "<path-to-your-code-folder>/<your-new-repo-name>"

```

### Step 5: Navigate into the new folder

```bash
cd <path-to-your-code-folder>/<your-new-repo-name>

```

### Step 6: Link to the original (Upstream)

We need to connect your copy back to the original ChatPRD repository so you can get updates.

*Note: The GitHub CLI often does this automatically. If you see "error: remote upstream already exists," that is good news! It means the link is already there.*

```bash
git remote add upstream https://github.com/ChatPRD/lennys-podcast-transcripts.git

```

**Verify your connections:**
Run this to see both `origin` (your repo) and `upstream` (the original).

```bash
git remote -v

```

### Step 7: Sync with the original

Pull down the latest transcripts from the original repository to ensure you are up to date.

```bash
git fetch upstream
git merge upstream/main

```

### Step 8: Clean up Mac system files (Optional but Recommended)

If you are on a Mac, run this command to prevent hidden system files (like `.DS_Store`) from cluttering your repository.

```bash
cat <<EOT >> .gitignore
# macOS specific
.DS_Store
.AppleDouble
.LSOverride
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# External drives
.Spotlight-V100
.Trashes
EOT

```

**Save this cleanup configuration:**

```bash
git add .gitignore
git commit -m "chore: add gitignore for macOS system files"

```

---

**You are now ready to build!** You have a clean, custom fork of the transcripts that you can easily update whenever new episodes are released.

---

## Part 2: Staying in Sync (Recurring)

Use this workflow when upstream adds new episodes or updates their documentation.

### When to sync

Check your GitHub repo page. If you see a message like "This branch is X commits behind ChatPRD/lennys-podcast-transcripts:main", it's time to sync.

**Sync periodically:**
- When you notice new Lenny episodes have been published
- Monthly or quarterly check-ins
- Before starting new RAG-o-Matic features that depend on fresh data

### Protective merge strategy

**Important:** If you've customized `README.md` or `CLAUDE.md` in your fork (like RAG-o-Matic does), you need to protect those files during the merge. This strategy ensures your custom documentation stays intact while pulling in upstream updates.

#### Step 1: Preview what's changed upstream

```bash
# Fetch latest from upstream (doesn't change your files yet)
git fetch upstream

# See what commits are new
git log HEAD..upstream/main --oneline

# See which files changed
git diff HEAD..upstream/main --name-only
```

#### Step 2: Merge with protection

```bash
# Start merge but don't auto-commit
git merge upstream/main --no-commit --no-ff

# Keep YOUR versions of custom files (ignore upstream changes)
git checkout --ours README.md CLAUDE.md

# Update the preserved transcript documentation
git show upstream/main:README.md > TRANSCRIPT_README.md
git show upstream/main:CLAUDE.md > TRANSCRIPT_CLAUDE.md

# Stage all changes
git add TRANSCRIPT_README.md TRANSCRIPT_CLAUDE.md README.md
```

#### Step 3: Review and commit

```bash
# Check what's about to be committed
git status
git diff --cached --stat

# Commit the merge
git commit -m "sync: merge upstream (preserve custom docs)"

# Push to your GitHub repo
git push origin main
```

### What gets updated

When you sync with this protective strategy:

- ✅ **New episodes** → Merged into `episodes/` directory
- ✅ **TRANSCRIPT_README.md** → Updated with upstream's latest README
- ✅ **TRANSCRIPT_CLAUDE.md** → Updated with upstream's latest CLAUDE.md
- ✅ **index/** → Updated topic files (if upstream changed them)
- ❌ **YOUR README.md** → Stays intact (your custom docs protected)
- ❌ **YOUR CLAUDE.md** → Stays intact (your custom docs protected)
- ❌ **Your custom files** → Untouched (explore.py, setup.sh, etc.)

### Troubleshooting sync issues

**"CONFLICT (content): Merge conflict in..."**
- This is expected for README.md if you've customized it
- The `git checkout --ours` command resolves this by keeping your version
- Just follow Step 2 to mark it as resolved

**"Already up to date"**
- You already have all upstream changes
- Nothing to sync right now

**"No new episodes, only documentation updates"**
- Upstream sometimes updates just their README (community project listings, etc.)
- The sync still works - you'll get those doc updates in TRANSCRIPT_README.md
- Your custom docs remain protected

### Alternative: Simple sync (if you haven't customized docs)

If you haven't created custom README.md or CLAUDE.md files, you can use the simpler approach from Part 1:

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

This will work fine for the original transcript repo fork without custom tooling.