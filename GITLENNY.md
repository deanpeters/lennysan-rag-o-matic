# GITLENNY.md

## How to Fork, Rename, and Sync "Lenny's Podcast Transcripts"

**Target Audience:** Non-programmers or anyone looking to build a custom tool on top of the original transcripts.

This guide explains how to take the original transcript repository, create your own copy (fork) with a custom name, and keep it linked to the original so you can pull in new episodes as they are released.

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