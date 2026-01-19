# User Journey
02-user-journey.md

This document describes the intended Product Manager experience for Version 1.0.

It is written as a narrative of actions, decisions, and outcomes.
It defines how the system should feel to use, not how it is implemented.

If implementation choices undermine this journey, the implementation is wrong.

---

## Primary User

The primary user is a Product Manager who:

- wants to explore a real product management question
- values evidence over opinions
- has limited engineering or notebook experience
- is cautious about breaking things
- is willing to follow clear, simple instructions

They are here to think, not to configure tools.

---

## Entry Point: Encountering the Contract

### What the user does
- Encounters the repository or is pointed to it
- Sees that a contract exists before code

### What the user is thinking
- This looks intentional
- Someone thought before building
- I am less likely to waste time or money here

### What the system communicates
- This repository is governed, not improvised
- There are explicit rules and boundaries
- AI tools are constrained, not in charge

### Success feels like
"I trust this before I even run anything."

---

## Stage 1: Approaching the Repository

### What the user does
- Clones the repository
- Opens it locally
- Skims the top-level structure

### What the user is thinking
- Where do I start?
- Is this safe to explore?
- Do I need to understand everything here?

### What the system must communicate
- You do not need to understand everything
- There is a clear, supported path
- Nothing dangerous happens by accident

### Success feels like
"I know where to begin."

---

## Stage 2: Discovering Topics and Notebooks

### What the user notices
- A notebooks/ directory
- One folder per topic
- One notebook per topic

### What the user is thinking
- This is manageable
- I can pick one thing to focus on

### What the system must communicate
- Topics are self-contained
- Reuse is encouraged
- Exploration is safe and reversible

### Success feels like
"This is designed for how I think."

---

## Stage 3: Choosing Reuse or Creation

The user reaches a decision point.

They can:
- reuse an existing topic
- create a new topic

### What the user is thinking
- Is it okay to use someone else’s work?
- What happens if I create something new?

### What the system must communicate
- Reuse is the default and encouraged
- Creation is explicit and intentional
- Nothing will be overwritten without confirmation

### Success feels like
"There is no wrong choice here."

---

## Stage 4A: Reusing an Existing Topic

### What the user does
- Navigates to a topic folder
- Opens the notebook

### What the user sees
- An orientation cell that explains what this notebook is
- Clear guidance on how to run it

### What the user is thinking
- I don’t need to set anything up
- I can just start reading and running

### What the notebook must do
- Explain itself before asking for action
- Encourage safe, top-to-bottom execution
- Avoid any setup or configuration steps

### Success feels like
"I can focus on the topic immediately."

---

## Stage 4B: Creating a New Topic

### What the user does
- Runs a single command to create a topic
- Provides a topic name
- Waits for the process to complete

### What the user sees
- Plain-language progress messages
- Confirmation that data was created
- A copy-paste command to open the notebook

### What the user is thinking
- This is doing real work
- I know when cost is being incurred
- I am not guessing what just happened

### What the system must do
- Perform all API calls up front
- Create all required files deterministically
- Leave no partial or ambiguous state

### Success feels like
"It did exactly what it said it would do."

---

## Stage 5: First Time Inside a Notebook

### What the user does
- Opens the notebook
- Reads the first cell

### What the user is thinking
- What is this notebook for?
- What do I need to know?

### What the notebook must communicate
- This is a guided workbook
- Python knowledge is not required
- Running cells is safe and repeatable

### Success feels like
"I understand how to use this without being taught Python."

---

## Stage 6: Exploring the Topic

### What the user does
- Runs the notebook
- Reads summaries and excerpts
- Pauses, skims, or rereads sections

### What the user is thinking
- This is interesting
- There is nuance here
- I am forming my own view

### What the notebook must support
- Clear separation between narrative and output
- Evidence with source context
- Explicit counterpoints or caveats

### Success feels like
"I am thinking more clearly than before."

---

## Stage 7: Learning Notebooks Implicitly

This learning happens without instruction.

### What the user learns
- How notebooks behave
- That rerunning cells is normal
- That reading matters as much as execution

### What the system must avoid
- Debugging tasks
- Hidden state
- Fragile execution order

### Success feels like
"I am no longer intimidated by notebooks."

---

## Stage 8: Returning and Reusing

### What the user does
- Reopens a notebook later
- Reruns it successfully
- Shares it with a colleague
- Copies a topic to explore a variation

### What the user is thinking
- I remember how this works
- I can build on this

### Success feels like
"This fits into my normal work."

---

## Stage 9: Sharing With the Community (Optional)

### What the user does
- Decides their topic might be useful to others
- Submits a pull request with a topic kit

### What the user is thinking
- This does not need to be perfect
- I am sharing thinking, not answers

### What the system must communicate
- Contribution is optional
- Imperfect work is acceptable
- Sharing reduces duplicated effort

### Success feels like
"I contributed without friction."

---

## End State

By the end of this journey, the user:

- trusts the system
- understands the topic better
- feels safe using notebooks
- sees value in reuse and sharing

If the user learns something but feels anxious about the tooling,
the journey has failed.

---

End of document
