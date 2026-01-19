# CLI UX Pack (0.x)
05-user-experience-pack.md

This document defines the canonical CLI experience for Version 0.x.

It exists to ensure that the CLI:
- feels safe to run
- teaches while it informs
- reduces intimidation
- reinforces good learning habits

If the CLI violates this UX, it violates the contract.

---

## Purpose of the CLI UX

For many Product Managers, this CLI is their first sustained interaction
with a local AI tool.

The experience must therefore:
- coach, not test
- guide, not impress
- reassure, not surprise

---

## Canonical CLI Flow

A standard query should feel like this:

~~~text
$ python explore.py "why safe sucks"

[search] Searching Lenny's podcast corpus...
[question] why safe sucks
[web] Web search fallback: ON (AUTO)

[thinking] ...

[answer]
--------------------------------------------------
# Why SAFe Sucks

Direct answer:
...

Indirect but relevant insights (inferred):
...

What's missing:
...
--------------------------------------------------

[sources]
- Guest: "Title" (YYYY-MM-DD)
  https://www.youtube.com/...

[model] Using <model>
        Cost: varies by model
~~~

This structure is non-negotiable.

---

## Required UX Behaviors

The CLI must:
- echo the user's question
- show when web search is enabled
- state when web search was skipped
- provide explicit sources
- admit missing or weak context

The CLI must not:
- hide costs
- imply web search happened when it did not
- output unstructured walls of text
- remove attribution

---

## Docker Search Warning (v0.8)

Docker search is an advanced, optional path. It is "free" but can require
extra setup, restarts, and troubleshooting. The CLI should warn users that
this path may be higher effort and encourage API search for simplicity.

---

## Error and Warning Style

Warnings should be:
- plain language
- action-oriented
- non-alarmist

Example:

~~~text
[warning] Web search requested but SERPER_API_KEY is missing.
    Search disabled. Add the key or use --web-search off.
~~~

---

## Pedagogic Output Rules

When possible, output should teach:
- what data was used
- what data was missing
- how the answer was formed

This is not fluff.
It is the primary user value.

---

## Verbosity Defaults

Verbose mode exists to support two users:
- PMs who want reassurance and guidance
- builders who want to inspect behavior

Default verbosity is defined in CONFIGS.yaml.
Users can override with `--verbose on|off`.

---

End of document
