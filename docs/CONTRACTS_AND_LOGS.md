# Contracts and Session Logs (Why This Repo Teaches)

This repo is pedagogic on purpose. We don’t just ship code, we capture intent and learning so PMs can see how the decisions were made, not just what the repo looks like after the cleanup crew left.

Think of this as the “trust and governance layer” of the project. It’s how we keep the work coherent as it grows, and how we make AI coding tools useful instead of chaotic. This is context engineering that makes sure your vibe-coding doesn’t get you vibe-fired for generating vibe-slop.

## Contracts

Contracts are how we make **constitutional governance** happen.

They paint a picture of the future by setting the guidelines, guardrails, goals, and non-goals for a **major version**. That way, when we use Codex (or Claude Code, or Cursor if we’re feeling spendy), we’re not just asking for code, we’re handing the agent a clear product spec for what the repo should become.

These contracts are written at the major-version level because they support an `/init` workflow like:

“Read and understand these documents, then give me a plan for how we approach building vN.N.”

Contract sets:
- [contracts/0.0-9.contract/](contracts/0.0-9.contract/) (covers the 0.x era)
- [contracts/1.0.contract/](contracts/1.0.contract/) (defines the future notebook path)

If code conflicts with a contract, the contract wins.

## Session logs

Session logs are the “how Dean made the sausage” archive.

They include the gory details: prompts, model responses, reasoning, debugging, and the real-time tradeoffs that happened while building. They’re not sanitized. They’re annotated with snarky commentary, PM tips, and the occasional programming trick, so you can learn the workflow, not just admire the outcome.

Start here:
- [deannotes/SESSION.0.1.STORY.md](deannotes/SESSION.0.1.STORY.md) (the original “Weekend at Lenny’s” build)

More logs:
- [deannotes/SESSION.0.5.LOG.md](deannotes/SESSION.0.5.LOG.md)
- [deannotes/SESSION.0.6.LOG.md](deannotes/SESSION.0.6.LOG.md)
- [deannotes/SESSION.0.75.LOG.md](deannotes/SESSION.0.75.LOG.md)
- [deannotes/SESSION_LOG_PROMPT.md](deannotes/SESSION_LOG_PROMPT.md)

These are teaching artifacts and decision history.

## Decision log

The decision log is the short list of big bets and the reasons behind them. If a change affects behavior, cost, or user trust, it belongs here so future you doesn’t have to play detective.

- [docs/DECISIONS.md](docs/DECISIONS.md)

## Idea parking lot

Not every idea belongs on the roadmap yet. We keep a low‑pressure idea log for anything that’s intriguing but not scheduled.

- [deannotes/IDEAS.md](deannotes/IDEAS.md)

Rule: if an idea gets scheduled for a specific release, tag it with the version in parentheses, like `(slated v0.85)`.
