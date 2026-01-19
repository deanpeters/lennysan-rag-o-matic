# Constitution Gap List (v0.1–v0.75 → v1.0)

Purpose: capture what the current Constitution **doesn’t yet encode** from the real v0.1–v0.75 decisions, so we can update Article text with lived governance.

Format: Article → Missing or under‑specified nuance.

---

## Article 1: Purpose
**Gaps**
- Explicitly name the **Lenny corpus RAG** focus and metadata‑backed attribution as the core of the product’s purpose.
- Include “one‑feature per version” as a **purpose guardrail**, not just a process rule.

## Article 2: Dual Nature of the System
**Gaps**
- Codify the **3‑part response format** (direct / inferred / missing) as part of pedagogy.
- Emphasize that pedagogic clarity includes **citations and metadata**.

## Article 3: Primary User
**Gaps**
- State the user’s fear of **hidden cost** and **silent API calls** explicitly.
- Call out that users want **plain‑language errors**, not stack traces.

## Article 4: Notebook as Core Interface
**Gaps / Conflict**
- Current reality is **CLI‑first** (v0.1–v0.75). Notebooks are **v1.0 future**.
- Needs a transitional clause: “Notebook‑first begins at v1.0; CLI remains canonical until then.”

## Article 5: One Topic, One Notebook
**Gaps**
- This is future‑state; add a “deferred until v1.0” note to avoid pre‑1.0 enforcement.

## Article 6: Self‑Contained Topic Kits
**Gaps**
- Not yet implemented; must explicitly defer to v1.0.

## Article 7: Build‑Time vs Learn‑Time
**Gaps**
- Add current rule: **web search is optional + gated** (AUTO vs ALWAYS).
- Explicitly call out **API keys must be present** or web search is disabled with warning.

## Article 8: Data Hierarchy
**Gaps**
- Include **CONFIGS.yaml** as canonical configuration data.
- Include **data/chroma_db** as derived state.
- Re‑state **YAML metadata preservation** as canonical truth.

## Article 9: Configuration Discipline
**Gaps**
- State explicitly: **CONFIGS.yaml is the default source of truth**; CLI overrides allowed.
- Secrets only via env vars; warn on missing keys.

## Article 10: Reuse Is the Default
**Gaps**
- Call out reuse of **prompt logs, release notes, and session logs** as first‑class reuse artifacts.

## Article 11: Sharing Is Encouraged
**Gaps**
- Add explicit **PR workflow** to upstream transcripts repo as a community behavior.

## Article 12: Community Cost Defrayment
**Gaps**
- Tie in **Serper quota protection** and why AUTO is conservative.

## Article 13: The System Must Coach
**Gaps**
- Add `--verbose` as the user‑controlled teaching dial.
- State that silence is only acceptable when user opts out.

## Article 14: Observability Without Overload
**Gaps**
- Define **quiet mode** (verbose off) and **log‑only mode** (indexing).

## Article 15: Narrow Vertical Slices
**Gaps**
- Add one‑feature‑per‑version as a constitutional rule (already practiced).

## Article 16: Delivery Over Perfection
**Gaps**
- Include the rule: **docs before tagging**, tests before docs.

## Article 17: Change Discipline
**Gaps**
- Explicitly include **doc updates first** and **release notes per version**.

## Article 18: Permanent Non‑Goals
**Gaps**
- Add “general web search engine” and “agentic research system” as non‑goals pre‑v1.0.

## Article 19: What Success Feels Like
**Gaps**
- Include “users trust citations and know what’s inferred vs direct.”

## Article 20: Supremacy Clause
**Gaps**
- Add that the **Constitution supersedes AI suggestions** (already practiced).

