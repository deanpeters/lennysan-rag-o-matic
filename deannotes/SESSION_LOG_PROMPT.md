# Session Log Capture Prompt (PM‑Pedagogic)

Use this prompt in Codex/Claude Code to generate a session log with verbatim prompts, reasoning, and PM lessons.

## Prompt

```
You are a documentation assistant. Create a session log file in deannotes/ named:
  deannotes/SESSION.<version>.LOG.md

Scope: capture our conversation from the prompt:
  "<START_PROMPT_VERBATIM>"
through the most recent prompt.

If the user did NOT provide a start prompt, recommend 2–3 likely start prompts based on the session context and ask which to use.

Requirements:
1) Capture every user prompt verbatim (warts and all).
2) For each prompt, write:
   - Response summary (what you decided + why)
   - Why‑not alternatives (what you explicitly rejected and why)
   - PM lesson (the product principle or governance rule applied)
3) Keep code diffs out of the log; summarize behavior changes instead.
4) Include a short header with approximate start/end times. If not provided, infer or estimate.
5) Use Markdown with clear sections and separators.

Output: write the file and confirm the path. Do not ask follow‑up questions unless something blocks you.
```

## Example Start Prompts (if user doesn’t specify)

- "so wht is the plan for v0.6?"
- "yes, let' draft the schema and example"
- "I don't think this CONFIGS helps us with future plans..."

