# User Journey (0.x)
02-user-journey.md

This document describes the intended Product Manager experience for the 0.x era.

It is written as a narrative of actions, decisions, and outcomes.
It defines how the system should feel to use, not how it is implemented.

If implementation choices undermine this journey, the implementation is wrong.

---

## Primary User

The primary user is a Product Manager who:
- wants trustworthy answers from a known corpus
- values evidence over opinions
- has limited engineering experience
- is cautious about hidden costs
- is willing to follow clear, simple instructions

They are here to think, not to configure tools.

---

## Stage 1: Encountering the Repo

### What the user does
- finds the repository
- reads the README
- sees the contract language

### What the user is thinking
- Is this safe to try?
- Will this cost me money accidentally?
- Do I need to be a programmer?

### What the system must communicate
- There is a golden path
- Costs are explicit
- The experience is teachable

### Success feels like
"I can try this without fear."

---

## Stage 2: Setup

### What the user does
- runs `./setup.sh`

### What the user sees
- clear progress messages
- a ready-to-use environment
- instructions for next steps

### What the user is thinking
- This is doing real work
- Nothing is hidden

### Success feels like
"I know what just happened."

---

## Stage 3: First Query

### What the user does
- runs `python explore.py "<question>"`

### What the user sees
- a clear question echo
- retrieval progress
- an answer with sources

### What the user is thinking
- Where did this come from?
- Can I trust it?

### What the system must communicate
- Evidence comes from the transcript corpus
- Sources are explicit and deduped
- Missing data is admitted

### Success feels like
"I trust the answer because I can see the sources."

---

## Stage 4: Model Switching

### What the user does
- runs `python explore.py --model <name> "<question>"`

### What the user is thinking
- Can I choose speed vs quality?
- Will this change cost?

### What the system must communicate
- model choice is explicit
- costs may vary by model
- defaults come from CONFIGS.yaml

### Success feels like
"I control the tradeoff."

---

## Stage 5: Optional Web Search

### What the user does
- runs `python explore.py --web-search on|always "<question>"`

### What the user sees
- whether search was engaged
- web sources listed separately
- a warning if API key is missing

### What the user is thinking
- Did it actually search?
- Did this cost me anything?

### What the system must communicate
- AUTO is conservative
- ALWAYS is a forced override
- missing keys disable search clearly

### Success feels like
"I know exactly what happened."

---

## Stage 6: Learning Through Output

### What the user sees
- Direct answer
- Indirect but relevant insights
- What's missing

### What the user is thinking
- This feels like a guided analysis
- I can see gaps and limitations

### Success feels like
"I learned, and I also know what I don't know."

---

## End State

By the end of this journey, the user:
- trusts the system
- understands the topic better
- feels safe running more queries
- can explain how the answer was formed

If the user learned something but feels anxious about the tooling,
the journey has failed.

---

End of document
