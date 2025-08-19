# A.I-Workflow-Showcase — Project Overview

Gauntlet AI showcases how engineers ship software with an AI-first approach, where the model writes most of the code and the engineer steers.  
The app ingests interview podcasts, transcribes and diarizes them, then extracts comparable "cards" that summarize each builder's approach.

## What this product is
- A comparison surface for AI-first engineering workflows
- Built from real interviews and transcripts
- Neutral about tools and techniques, no required buzzwords

## Unified Workflow Cards (in order)

### 1) Planning & Scoping
What they aim to build, the constraints they agree to, and the definition of done.  
We capture goal, assumptions, and success checks in plain language.

### 2) Context Management
How they prepare and feed information to the model, how they keep a single source of truth, and how they maintain consistency across sessions.

### 3) Codegen Loop
How they steer the model to write code.  
Prompt pattern, interface of choice, edit granularity, and when they accept or rewrite.

### 4) Verification & Safeguards
How they check that the output is correct and safe before it lands.  
Fast runnable checks, simple tests or smoke runs, basic reviews that block merges.

### 5) Iteration Style
How they evolve the solution over time.  
Their cadence, unit of change, refactor triggers, and how they reuse or adjust prompts.

### 6) Deployment & Delivery
How changes reach users.  
PR flow, CI touchpoints, release surface, flags, and rollback habits.

## Extraction principles
- Pull facts from what the interviewee actually says
- Prefer short, concrete statements over tool names
- Do not require special keywords, infer from context
- Keep each card self-contained and comparable across builders

## Output
A structured profile with the six cards above, optional short quotes, and a compact tool list for context.