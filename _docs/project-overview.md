** Project Context for AI**

We are building a web app that showcases how different top AI builders create software using AI tools. Each builder has their own unique workflow, but the app presents them in a unified, comparable format.

The goal is to extract from any transcript, podcast, or interview the core elements of the builder’s process and present them visually in the same structure so users can quickly compare techniques.

The unified structure for each workflow is:

Planning & Scoping – How they define goals, constraints, and requirements before building.

Context Management – How they structure prompts, manage memory, or organize information for AI.

Guardrails & Validation – How they ensure correctness, reliability, and quality (tests, reviews, constraints).

Iteration Style – How they refine, test, and evolve their work over time.

Tool Stack – All tools they use, each labeled with category and role.

Integration & Orchestration – How they connect AI with other tools, APIs, or systems.

Deployment & Delivery – How they share the result, from demos to production launches.

The app is not teaching general AI tool usage — it focuses on showing practical, real-world AI-first development workflows from individual builders, organized by these categories.

Input: Raw transcript or text of the builder describing their process. (We will transcribe a podcast using tts)

Output: Structured profile matching the above categories, plus optional quotes, code snippets, and tool lists.