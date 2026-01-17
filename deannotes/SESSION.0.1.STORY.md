# Weekend at Lenny’s v0.1

## A PM Code Crawl to a Proof-of-Life

**TL;DR:** I took Lenny’s transcript corpus + Claire Vo’s markdown structure and, over one sleep-ruining night, built a tiny local RAG “Proof of Life” so non-programmer PMs can query the corpus with Claude Desktop / ChatGPT Desktop today: and hand it off to Claude Code / Codex next.

It’s Friday night. It's 1:20 AM and I wake up in the middle of the night because, well, I'm older than dirt.

The house is quiet in that *too-quiet* way: like it’s watching you.

Somewhere in the distance a refrigerator hums like it’s plotting.

And on my nightstand, my phone is glowing with the kind of temptation that has wrecked more weekends than tequila:

> “A clean, beautifully structured transcript corpus… just sitting on GitHub.”

All week I’d been side-eyeing it.

The way you side-eye a suspiciously cheap “AI Strategy” workshop.

The way you side-eye a backlog that claims it’s “prioritized.”

Because I knew what it *really* was:

- 300+ episodes of product wisdom
- pre-packaged into markdown
- with metadata that actually lets you *trust* what you’re reading

In other words: a PM’s dream, and a perfect trap.

By 1:25 AM, I’m awake. Not “rested” awake.

More like “the goblins of curiosity are holding a standup in my skull” awake.

So I do the only reasonable thing:

I start building a RAG tool with Claude… from my phone… in bed… like a responsible adult.

### What you’re about to watch happen

This is a pedagogic field report for non-programmer PMs who want to try:

- Claude Desktop / ChatGPT Desktop today
- Claude Code / Codex tomorrow
- and (eventually) local models without turning into a full-time developer

You’ll see:

- my prompts, verbatim
- the tiny nuances that make the model behave
- the moments where “PM thinking” saves the product
- and the furballs that show up at 3:33 AM to remind you reality is undefeated

**Time (ET):** 1:25 AM – \~5:00 AM\
**Role:** Product Manager (Recovering Engineer)\
**Device Path:** iPhone (start) → MacBook Pro + Claude Desktop (finish)\
**Goal:** Ship `v0.1` “Proof of Life” before the sun shows up and judges me.

This is not a programmer’s write-up.

It’s a PM story about building *just enough* infrastructure to get value from a corpus, without accidentally inventing a new religion called “Tooling.”

---

## Prologue: The week-long simmer

All week, I’d been admiring two things like a PM raccoon staring at shiny objects behind a fence:

1. Lenny’s transcript GitHub repo (the corpus)
2. Claire Vo’s conversion work (the structure)

It was the kind of “I can’t wait to tackle this over the weekend” thought that sounds wholesome.

It is not wholesome.

It is the opening scene of a horror film.

---

## 1:25 AM: “So this dropped earlier this week…”

I wake up (because I’m old as dirt) and immediately do what every healthy adult does:

I grab my phone and start thinking about a repo that “blessed the PM community.”

**Prompt (1:25 AM):**

```text
So this dropped earlier this week
https://github.com/ChatPRD/lennys-podcast-transcripts
```

Somewhere between insomnia and “just one quick look,” my PM brain goes:

> “That’s not just transcripts. That’s a corpus.”

> “That’s a product manager’s research assistant… if I can RAG it.... and later add reasoning and research to it...”

And then the real fun begins.

---

## 1:30 AM: The first fork-in-the-road: “Is this even possible?”

**Prompt (1:30 AM):**

```text
Actually I think I want to fork the repo into perhaps an RAG type project using Claude Code and open source tooling. Is that even possible on my MacBook Pro?
```

Notice what I *didn’t* say:

- I didn’t ask for LangChain.
- I didn’t ask for microservices.
- I didn’t ask for a 14-step “agentic architecture.”

I asked one thing:

**Can I do this locally, on my Mac, without summoning a yak-shaving demon?**

### PM prompting technique: start with feasibility, not features

If you’re not sure the thing is even buildable, feature brainstorming is just… creative writing.

---

## 1:30 AM: Security brain kicks in (thankfully)

Claude mentions API usage and I do what every “recovering engineer” PM should do:

**I pounce on security.**

**Prompt:**

```text
Once I have this set up, would I be able to switch models with API keys that I keep stashed as environment variables?
```

Translation:

“I’m happy to build. I’m not happy to leaky keys.”

### PM prompting technique: bake in guardrails early

If you wait until “later” to address keys, logs, and local files…

“later” becomes “post-incident.”

---

## 1:30 AM: Maintenance brain kicks in

Because “a cool weekend project” is how a lot of future maintenance debt is born.

**Prompt:**

```text
Is there some way that once I have this set up I can create notebooks on different topics?
```

Then I push on accessibility and cost, because this is for not-so-tech-savvy PMs, not just me:

**Prompt:**

```text
Is the notion or obsidian path open source? Or do I need to think about using Google Collab approach to notebooks or Jupiter notebooks
```

### PM prompting technique: ask “how do we keep this cheap for learners?”

It’s easy to build something that *you* can run.

It's easy to build because much of the UX is offloaded to other tooling made for this job.

It’s harder (and more valuable) to build something your learners can run without a second mortgage.

---

## 1:37 AM: The “vision” prompt (a.k.a. the anti-scope-drift anchor)

Claude comes back with feature suggestions, and I can feel the drift starting.

So I drop **the big anchor prompt**.

**Prompt (1:37 AM):**

```text
I want to create some sort of system that encourages and makes it relatively easy for someone to take the GitHub fork that we are going to create, run it on their own MacBook for now, and windows for later, and be able to set up topical projects or notebooks that effectively allow them to explore the day via the RAG in combination with their choice of model

Basically, I want a product manager to be able to use this corpus as a very low touch low technical way of getting high quality feedback

I also want people to be able to avoid having to churn up CPU and tokens creating things like Claude projects or Gemini gems when they want to explore topic of product management against the Lenny corpus, which they might expand later with other .md subdirectors of wisdom.

For example, we could take an add productside webinars and podcasts and create another subdirectory to help expand this body of wisdom in the future
```

This prompt does three important PM things:

1. Defines the user (PMs, not engineers)
2. Defines the value (low-touch, low-tech, high-quality feedback)
3. Defines the cost and complexity enemy (CPU churn, token churn, “projects/gems rebuilding”)

---

## 1:47 AM: “Let’s scaffold the session” (setup + CLAUDE.md)

I’m still on my phone. Still not writing to files, though I know I should.

Still, I ask to see scaffolding that will work when I get to a real machine.

**Prompt (1:47 AM):**

```text
I wonder if we shouldn't first create a bash setup.sh that a person could run to do the GitHub and directory work? And maybe have a Claude.md  So when we Open up Claude code from the command line We can point it at the file to help kickstart the session?
```

This is a pattern I want every PM to steal:

> Use AI to create the rails, not just the train.

Setup scripts. Session docs. Repeatability. On-ramps.

---

## 1:51–1:52 AM: Brand battle: “Don’t change the name on me.”

Claude starts suggesting boring project names (because of course it does).

And I do what any responsible product person does:

I defend the brand like it owes me money.

**Prompt (1:51 AM):**

```text
Don't change the name on me. Because what happens if we add other podcasts and webinar materials l? You just rebranded my name for the project and by doing so put a limit on it.
```

Then I draw the line:

**Prompt (1:52 AM):**

```text
No, I realize we have to think like a programmer in this session, but we also have to think like a product manager
`LennySan RAG-o-Matic` is the name of this project. Doing this by design
```

### PM prompting technique: be explicit about product decisions

Models will “helpfully” optimize you into blandness.

If you care about positioning, you must assert it.

---

## 1:59–2:10 AM: Proof-of-Life as a weapon against scope creep

I introduce future interface ideas (CLI, Jupyter, Streamlit) but label them as future scope.

**Prompt (1:59 AM):**

```text
I like this. One of the other things I want to be able to do with this is work in a localized large language model setting in the future. That is future scope just like windows is future scope.

I think in the readme we also need to make clear about what type of interface we think we're going to have with each of these topical notebooks we create. I'm talking about telling people we're going to use Jupyter or Steamlit or CLI
```

Then I define the incremental releases like a PM who has been burned by bloat before:

**Prompt (2:07 AM):**

```text
0.01 is me just getting the baseline repo published so we can start capturing work during this session.
0.1 is the minimal, proof-of-life CLI with either an open AI API or anthropic Claude API
```

Then the money line:

**Prompt:**

```text
Let's split 0.1

0.01 Establish the beachhead
0.1 Show Proof of life
0.5 Then show proof of concept

Remember we get more done faster when we focus on less.

You're going to need to learn to be very narrow with your vertical slices working with me.
```

And I explicitly target cost:

**Prompt (\~2:10 AM):**

```text
I also think as we work on the proof of life and proof of concept we can use a very very very inexpensive model within the anthropic API

We're just looking for smoke signals not spectacular responses from the API  just yet
```

### PM prompting technique: name the release stages

“Proof of Life” is magic phrasing, especially when managing up, because it tells everyone:

- We are verifying the organs work.
- We are not building a personality yet.
- Nobody gets to sneak 'it's just a feature' into my bloodstream.

---

## 2:50 AM: Phone down. Laptop up. “Claude Desktop, you’re driving now.”

At some point, reality hits: I need file access. I need a repo on disk.

So I cast off the blankies and put on a warmer shirt.

(It still snows here in Raleigh, NC ... and I know it's gonna be chilly)

I migrate to Claude Desktop and hand it a path.

**Prompt (2:50 AM):**

```text
Okay, so I've stopped this session on my phone and am now on Claude Desktop.

I have updated the `claude_desktop_config.json` so you should have access.

I went ahead and forked and renamed and published the repo in:

"/Users/deanpeters/Code/lennysan-rag-o-matic

You can see how I did it in the GITLENNY.md file I created.

Note, within that same path, there is already a README.md and CLAUDE.md so first, we should likely rename those files?
```

### PM prompting technique: when switching tools, restate ground truth

When you move from phone → desktop (or ChatGPT → Claude → Claude Code), assume the model’s brain got rebooted.

Give it:

- the path
- the constraints
- the “what exists already”
- the next action

---

## 3:09 AM: The biggest save of the night: metadata

Claude generates `index_corpus.py` and my spider-sense tingles as I read it line-by-line.

Because I know the transcripts weren’t just text.

They had YAML frontmatter metadata, the good stuff.

So I ask the question that prevented a broken project model:

**Prompt (3:09-ish):**

```text
Hey, for our setup.sh and index_corpus.py ... are we adding to our RAG the metadata that Clair Vo adorned the transcripts when she also converted them to .MD files? I want to make sure we're not overlooking that valuable asset.
```

This is not a nerd detail.

This is a user trust detail.

Because without metadata:

- you can’t cite who said what
- you can’t filter by guest/date
- you can’t build “topic notebooks” that behave

### PM prompting technique: ask “are we using the valuable parts of the source?”

AI will happily index the “easy” parts and skip the “meaningful” parts.

Your job is to protect the meaning.

---

## 3:22 AM: “User experience matters” (status, sleep, logs)

Now I’m thinking about the non-coder PM who runs `setup.sh` and stares at a blinking cursor like it’s a feature hostage negotiation.

So I prompt for UX:

**Prompt (\~3:22 AM):**

```text
Hey, for our setup.sh and accompanying python files ... I would image that it's going to take some time to run. Do I get status updates on screen to a) see we're still processing and b) keep the system from going into a sleep mode as I go back to sleep and dream about the 0.1 test from the CLI about TAM/SAM/SOM theater and/or what interview questions Lenny might have for Rina Alexin, the awesome CEO of Productside?
```

Then:

**Prompt:**

```text
setup Logs to perhaps capture if crap happens we have them to debug?
```

This is a product move, not a developer move.

Progress indicators and logs are empathy in code form.

---

## 3:33 AM: The first furball: dependency rot (classic)

By 3:30 we’re ready.

By 3:33 the universe reminds me I haven’t earned joy yet.

**Console capture:**

```text
✅ Dependencies installed

🔍 Indexing corpus in ChromaDB...
This will take 5-10 minutes.

💡 To prevent your Mac from sleeping during indexing:
   We'll use 'caffeinate' to keep the system awake.

☕ Perfect time for that coffee break!

Traceback (most recent call last):
  File "/Users/deanpeters/Code/lennysan-rag-o-matic/index_corpus.py", line 15, in <module>
    from langchain.schema import Document
ModuleNotFoundError: No module named 'langchain.schema'
```

My perfectly reasonable reaction:

> “do I need to brew or pip or what?”

### PM lesson: dependency errors are not failure, they’re information

They’re the product telling you what assumptions you made about your environment.

Also: LangChain moved things again.

Of course it did.

---

## \~3:54 AM: Proof of Life achieved… and it’s “stupid right now” (good!)

After multiple rounds of “fix thing, run thing, watch it explode differently, copy error messages to claude for analysis and fixes,” we get to a working state.

**Prompt (\~3:54 AM):**

```text
Success ... see attached console capture.
Some thoughts.
1 ) can we supress the annoying deprecation errors?
2) can we instruct the CLI to engage a web search (via the model) if they can't find the info? You'll see what I mean when I issue the TAM-SAM-SOM and Rina Alexin, Productside CEO questions.
```

This is exactly how “Proof of Life” should feel:

- it works
- it’s ugly
- it reveals the real next work

If your v0.1 feels polished, you probably overbuilt it.

---

## 4:30 AM: Costs (because I’m a PM, not a chaos gremlin)

I check actual API costs and write them down like a responsible adult. Besides, all 5 of my loyal readers are gonig to want to know this:

- Total project: **\~\$0.16**
- 5 queries: **\$0.007**
- Extrapolated 1,000 queries: **\$1.40**

Then the desktop-assistant reality check:

**Prompt (4:38 AM):**

```text
You knucklehead ... okay this entire session ... consumed 90% of my session limit an ~20% of my weekly session limit for the Pro plan. We need to add that to our docs.

Then it's time for bed.
```

### PM lesson: cost has TWO meters

1. API dollars
2. tool limits / quota

Both matter.

---

## \~5:00 AM: Ship it. Document it. Get out.

I end with the kind of “do this so you don’t break yourself later” release checklist that PMs secretly love.

**Commit + push script:**

```text
# Navigate to repo
cd ~/Code/lennysan-rag-o-matic

# Deactivate venv if active
deactivate

# Check status (see what's changed)
git status

# Add everything
git add .

# Commit with comprehensive message
git commit -m "feat: v0.1 complete with session story

- Created deannotes/ directory for article series
- Moved session narrative to SESSION.0.1.STORY.md
- Fixed ASCII art rendering in README
- Added activate.sh convenience script
- Updated all cost data with actual measurements
- Platform limits: 90% daily, 20% weekly
- Timeline: 1 AM - 4:40 AM (3h40m total)
- Result: 303 episodes, 37,450 chunks, full metadata

Ready for v0.5 model switching."

# Push to GitHub
git push origin main

# Verify it's there
git log -1 --oneline

# You're done!
echo "✅ v0.1 shipped! Go to bed! 😴"
```

Reader, I did not go to bed.

I negotiated with bed.

---

# What I want non-programmer PMs to learn from this weekend

## 1) Your prompts are your product decisions

If you don’t state the user, value, and constraints, the model will invent them for you.

## 2) “Proof of Life” beats “MVP” when you’re establishing scope by appetite

Name the stage. Guard the stage.

## 3) Read the generated stuff before you run it

That metadata moment is the difference between a toy and a tool. That goes 2x for the security stuff.

## 4) Add UX to scripts: progress + sleep prevention + logs

Because your user is a human, not a CI pipeline.

## 5) Measure cost like a PM

Not vibes. Numbers.

---

# Next episode teaser: v0.5 handoff

This is the part where “Claude Desktop wrote files” hands off to:

- Claude Code (or Codex later)
- model switching
- cleaner dependency strategy
- better retrieval behaviors

But not tonight.

Tonight, we shipped Proof of Life.

✅ v0.1 shipped. Go to bed.

