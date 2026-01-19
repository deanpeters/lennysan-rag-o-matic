# 0.x Contract Consistency Check
00-consistency-check.md

This document verifies that the 0.x contract documents are internally consistent,
non-contradictory, and collectively enforceable.

Its purpose is to prevent drift, ambiguity, and accidental violations before
any code is written or modified.

This is a validation artifact, not a design document.

---

## Documents in Scope

This consistency check covers the following files in `contracts/0.0-9.contract/`:

1. README.md
2. RELEASE_NOTES.md
3. INSTRUCTIONS_FOR_CODEX.md
4. 01-repo-reality-and-scope.md
5. 02-user-journey.md
6. 03-constitution.md
7. 04-implementation-brief.md
8. 05-user-experience-pack.md

All checks below assume these documents.

---

## Contractual Intent (Aligned)

### Primary Purpose
All documents agree that the repository is:
- a pedagogic tool first
- a practical research tool second

No document positions the system as:
- a notebook-first platform
- a general web-research engine
- a dashboard or agentic system

Intent is consistent.

---

## Version Semantics (Aligned)

All documents treat 0.x as:
- CLI-first and stable
- governed by CONFIGS.yaml
- narrow in scope with one feature per release
- safe and teachable for PMs

No document implies:
- notebook workflows (reserved for 1.0)
- automated orchestration
- UI-first experiences

Version semantics are consistent.

---

## User Persona and Journey (Aligned)

Across README, User Journey, Constitution, and UX Pack:
- Primary user is a Product Manager
- Limited engineering experience is assumed
- Safety, clarity, and confidence are prioritized

No document contradicts this persona.

---

## Metadata and Attribution (Aligned)

All documents agree:
- YAML metadata must be preserved end-to-end
- sources must always be printed with guest/title/date/URL

No document weakens attribution.

---

## Configuration Discipline (Aligned)

All documents agree that:
- CONFIGS.yaml is canonical
- environment variables are for secrets only
- no parallel config files are allowed

No contradictions found.

---

## Web Search Fallback (Aligned)

All documents agree:
- web search is optional and controlled
- AUTO mode is conservative
- ALWAYS mode exists for testing
- missing API keys disable search with warnings

No document implies mandatory web search.

---

## Known and Intentional Tensions (Accepted)

The following tensions are acknowledged and acceptable:
- AUTO fallback may skip web search even when users want it
- ALWAYS may incur cost and quota faster

These are handled via explicit overrides and documentation.

---

## Conclusion

The 0.x contract documents are:
- internally consistent
- mutually reinforcing
- enforceable by humans and AI tools
- aligned with pedagogic and research goals

No blocking contradictions were found.

---

End of document
