# Flowdex Workflow Extraction — Example (Palmer, Interviewer A)

> This file is a formatting and content-quality reference for the extractor.  
> Quotes are verbatim from Interviewer (A) with timestamps pulled from the provided transcript.

## Planning & Scoping
**Tools used in this phase (AI only):** Grok, Perplexity

**Summary (2 sentences):** Plans **outside the IDE**. Co-plans in Grok, then asks it to **summarize the conversation** into a short project overview and follows a ~12-step setup guide to scaffold the repo.

### Card 1 — Project overview first
- **Approach:** Start with a written overview/spec before coding; keep it concise and clear.
- **Quote:** “Before you start your project, you should have a document that clearly outlines what you're building.” — [07:58–10:52]
- **Artifact:** `/_docs/project-overview.md` (short overview/spec)

### Card 2 — 12-step setup (scaffolding)
- **Approach:** Use a step-by-step guide (~12 steps) to generate starter docs and structure.
- **Quote:** “It's a step by step, essentially prompt guide… **12ish steps** that you should go through to get the entire… **scaffolding** put together for your project.” — [04:49–07:47]
- **Artifact:** `/_docs/new-project-setup.md` (overview → user flow → tech stack → UI/theme rules → project rules → phase checklist)

### Card 3 — Co-plan in Grok; Perplexity for quick checks
- **Approach:** Co-plan in Grok, then summarize into docs; use Perplexity for quick factual lookups.
- **Quote:** “I'll typically dump it into **Grok**… we form the document as we go and then anytime I'm doing this kind of setup step, I'll have it **summarize the conversation at the end**.” — [35:25–37:33]
- **Quote:** “I've **been using Perplexity** just because it's quick and simple for… answering basic questions…” — [35:25–37:33]

---

## Context Management
**Tools used in this phase (AI only):** Cursor

**Summary (2 sentences):** Puts all context/rule docs in a top-level `/_docs` folder so they’re easy to attach. In Cursor, he distinguishes **attached (persisted)** vs **mentioned (one-off)** files, and typically keeps **Tech Stack** + **Project Overview** attached for multi-turn work (adding **Theme Rules** for UI tasks).

### Card 1 — `_docs` at the top
- **Approach:** Name the docs folder with an underscore so it stays at the top; store all rule/context docs there.
- **Quote:** “I have this docs folder. **I name it with an underscore just so it stays at the top** of the hierarchy.” — [07:58–10:52]
- **Artifact:** `/_docs/` (overview, user flow, tech stack, theme rules, project rules, phase/checklist docs)

### Card 2 — Attach vs mention
- **Approach:** Attach core docs in the chat header for persistence; mention files inline for one-off tasks.
- **Quote:** “**Reference a file** if you want it just used for a single message… however, if you want this **persisted** through the entire chat, you should **add it up here** [header].” — [38:04–50:24]

### Card 3 — Rules hierarchy (User Rules + Cursor Rules)
- **Approach:** Use **User Rules** for broad style/structure; **Cursor Rules** for tech-specific guidance.
- **Quote:** “**User rules**… apply very broadly… **They keep a very consistent structure**.” — [16:08–18:01]
- **Quote:** “Cursor… announced [the monolithic rules file] is deprecated and that you should be using **cursor rules**… the ability to manage these more fine grained rules is really important.” — [12:52–15:54]
- **Artifact:** `/.cursor/rules/*.mdc` (e.g., Drizzle rules, GitHub CLI example)

---

## Codegen Loop
**Tools used in this phase (AI only):** Cursor, Custom Modes (Plan/Scaffold)

**Summary (2 sentences):** Keep **one chat per task/feature**. Instruct Cursor to **use tools to explore** the codebase before editing; custom modes can scaffold, but he prefers a two-way iterative loop.

### Card 1 — One chat per task/feature
- **Approach:** Scope each chat tightly; start a new one when the goal changes or context gets long.
- **Quote:** “**Keep chats scoped to tasks or features…** If your chats are covering more than one feature, just **make a new one. Always.**” — [50:29–51:45]

### Card 2 — Explore with tools first
- **Approach:** Tell the agent to **use tools to explore** (grep/read) before writing or editing code.
- **Quote:** “**Use tools to explore the code base**… I always have it explore the code base first… I even have that in my user rules.” — [51:50–53:21]

### Card 3 — Custom modes for repeatable loops (optional)
- **Approach:** A **scaffold** or **plan** mode can one-shot documents/structure; still prefers conversational iteration.
- **Quote:** “I created this **scaffold mode**… it’ll go ahead and **produce all of these files** just from the project overview… **I don’t use it often** because I like having a two-way street.” — [23:33–31:05]
- **Artifact:** Cursor Custom Mode settings (e.g., Plan/Scaffold)

---

## Verification & Safeguards
**Tools used in this phase (AI only):** Cursor

**Summary (2 sentences):** Enforces **structural guardrails** (keep files ~under 500 lines; add JSDoc/TS-doc blocks) to help both humans and the agent. When problems repeat, he creates a **brief rule/doc** to prevent the same mistake; for tricky bugs, he favors fresh context and **restore checkpoint**.

### Card 1 — Structural guardrails
- **Approach:** Keep files under ~500 lines; add JSDoc/TS-doc blocks so code is easy to include and understand.
- **Quote:** “I keep **all my files under 500 lines**… Then I also want to do these **JSDOC and TS doc** comment blocks above all my files, functions…” — [23:33–31:05]

### Card 2 — Prevent repeat mistakes with a doc
- **Approach:** If the agent repeats an error (e.g., Yarn vs npm), write a short doc/rule and attach it next time.
- **Quote:** “If I've gone through several times where it's trying to use Yarn… I'll say, **we're using npm**. **Create a document** that explains what we're using and why… so it **doesn't make the same mistake again**.” — [56:59–57:06]

### Card 3 — Debug hygiene: fresh context + checkpoints
- **Approach:** For older bugs, start a new chat, explore with tools, and use **restore checkpoint** to revert bad paths.
- **Quote:** “**Always start with clean context**… If you don’t reach a resolution… **restore your checkpoint**… try it again from the start.” — [53:21–53:23, 58:25–58:51]

---

## Iteration Style
**Tools used in this phase (AI only):** Cursor

**Summary (2 sentences):** Prefers **small, reversible increments** and avoids long chats. Uses **phase checklists** so the app stays runnable after each phase.

### Card 1 — Small, reversible steps
- **Approach:** Many small iterations beat big leaps; keep each step testable/reviewable.
- **Quote:** “I like having it be a **two-way street**… but **typically** I recommend **splitting it up as much as you can**.” — [23:33–31:05, 50:29–51:45]

### Card 2 — Avoid long chat drift
- **Approach:** Don’t let chats accumulate conflicting context; prefer new chats over heavy summarization.
- **Quote:** “If a chat gets sufficiently long… I **don’t** use the summarize feature super often… **just make a new one**.” — [51:46–53:21]

### Card 3 — Phase checklists keep it shippable
- **Approach:** Structure work into setup → MVP → expansions so it remains runnable end-to-end.
- **Quote:** “I want a **working product through every phase**… so the thing actually **works all the way through delivery**.” — [23:33–31:05]
- **Artifact:** `/_docs/phase-checklist.md` (setup/MVP/expansion phases)

---

## Deployment & Delivery
**Tools used in this phase (AI only):** None stated

**Summary (2 sentences):** Designs for **deliverability by structure**—phased checklists ensure a runnable app at each stage through delivery. Also maintains a lightweight **GitHub CLI issue flow** in Cursor to anchor work items.

### Card 1 — Deliverable after each phase
- **Approach:** Use phased checklists so each phase ends in a runnable artifact (setup → MVP → expansion).
- **Quote:** “Each one builds on itself… **I want a working product through every phase**… so it **works all the way through delivery**.” — [23:33–31:05]
- **Artifact:** `/_docs/phase-checklist.md`

### Card 2 — Lightweight GitHub CLI issue flow (in Cursor)
- **Approach:** Keep a Cursor rule doc for GitHub CLI to create/read/resolve issues directly in the IDE.
- **Quote:** “I made this **GitHub CLI example** document… it’ll **create issues, read issues, and even resolve issues**… almost like having a **miniature Devin** in your code base.” — [12:52–15:54]
- **Artifact:** `/.cursor/rules/github-cli-example.mdc`