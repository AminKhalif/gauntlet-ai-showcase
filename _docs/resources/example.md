Below is a recommended order for creating these documents so each naturally builds upon the previous. This sequence ensures we first set the project context (overview, user flow, tech decisions), then define our rules (tech stack, UI, theme, code organization), and finally outline our phased approach and detailed workflows.
project-overview.md

Establish overall project purpose, scope, and goals.
user-flow.md

Clarify how users will interact with the application (landing, registration, navigation, redirects, registration, etc).
tech-stack.md

Describe the core technologies used (Node, Next.js, TypeScript, etc.) and their roles.
ui-rules.md

Define visual and interaction guidelines for building components (including design principles and component behaviors).
theme-rules.md

Establish theming foundations (colors, typography, etc) to be incorporated into UI development.
project-rules.md

Outline folder structure, file naming conventions, etc.
./phases/ (subdirectory within _docs/)

Outline the different phases of the project, and the different tasks and features we'll need to complete in order to complete our goal. Each feature (or group of features) should have its own phase document.
Below are recommended steps/prompts for creating these files from scratch, with only the project overview to guide you.
PROMPT:
Use @project-overview.md to create a document called `user-flow.md`, which should define the user journey through different segments of the application.

The user journey should take into account the different features the app has & how they are connected to one-another. This document will later serve as a guide for building out our project architecture and UI elements.

Ask clarifying questions if needed-- we don't want any embellishments or assumptions.
NOTE: If you have any stack preferences, mention them here. For nearly any web app with AI, I'd personally recommend TypeScript (language), React (UI library), Tailwind CSS (utility-first CSS framework), Shadcn (component library built on Radix UI and Tailwind), Next.js (full-stack React framework with routing), Supabase (database and authentication), and Vercel (deployment/hosting).
Use @project-overview.md and @user-flow.md to make recommendations for our stack. I already know I want to use ___, ___, and ___ (e.g. TypeScript, React, Tailwind).

For each part of our stack, propose and describe an industry standard and a popular alternative. We will work through the list together to determine what we'll use for the project.
USER ACTION: Look through the proposed stack and think about what you want to pick. For ones you're unsure of, ask about pros/cons, see what's most compatible with the rest of the stack, etc. When you're done, ask the AI to output the decisions in a markdown file called tech-stack.md.

PROMPT:

Update @tech-stack.md to cover all best-practices, limitations, and conventions for using the selected technologies. It should be thorough, and include important considerations and common pitfalls for each one.
NOTE: If you don't know much about UI, UX, design, or theming, this is a great opportunity to learn. Ask questions about common design principles, styling, etc, for the type of application you're building. If you have persona preference, obviously voice them here as well.
Walk me through some common design principles for this type of application, and recommend some possible styles (e.g. "minimalist", "glassmorphic", "neumorphic", etc.) that fit what we're building.
Observe @project-overview.md and @user-flow.md for context about the project to guide your recommendations.
NOTE: Edit the blank spaces in the prompt to suit your desires for the project.
I want my project to be ____ (mobile-first, responsive, animated, iconographic, etc).

Also, I have decided I want my theme to be ____ (minimalist, glassmorphic, neumorphic, etc).

Use @project-overview, @user-flow.md, and @tech-stack.md to put together two new files, called `ui-rules.md` and `theme-rules.md`. The former should focus on common design principles for our application to follow, while the latter should outline all the colors and styles we're using to create a consistent theme across our application.
PROMPT:
We are building an AI-first codebase, which means it needs to be modular, scalable, and easy to understand. The file structure should be highly navigable, and the code should be well-organized and easy to read.

All files should have descriptive names, an explanation of their contents at the top, and all functions should have proper commentation of their purpose and parameters (JSDoc, TSDoc, etc, whatever is appropriate).
To maximize compatibility with modern AI tools, files should not exceed 500 lines.

Use @tech-stack.md, @user-flow.md, @project-overview.md, @ui-rules.md, and @theme-rules.md to put together a new file called `project-rules.md`, which touches on our project's directory structure, file naming conventions, and any other rules we need to follow.
PROMPT:
We need to define the tasks and features to build our project, progressing from a barebones setup to a minimal viable product (MVP), to a feature-rich polished version.

Create an iterative development plan for the project, outlining the tasks and features needed to reach these phases.

Rules to follow:
- Start with a 'setup' phase: a barebones setup that functions at a basic level but isn’t fully usable (e.g., a minimal running framework or structure).
- Define an 'MVP' phase: a minimal, usable version with core features integrated (e.g., essential functionality that delivers the project’s primary value).
- Add additional phases as needed: enhancements to improve and expand the MVP (e.g., advanced features, polish, or scalability).
- Each phase gets one document, detailing its scope and deliverables.
- Focus each phase on delivering a functional product, combining essential features into a cohesive whole (e.g., key components that work together).
- List features with actionable steps (max 5 steps per feature; break down into smaller features if longer).
- Keep phases iterative—each builds on the previous phase, enhancing a working product.

Place these documents in `_docs/phases/`. Review @project-overview.md, @user-flow.md, @tech-stack.md, and @project-rules.md to gather relevant context about the project and its features.
USER ACTION: Make a brief Agent Rules file, which will be a list of rules for the agent to follow (duh). It's recommended that you place this in your Cursor User Rules (CMD + Shift + P > Cursor Settings > Rules > User Rules), and/or make a Cursor Notepad (There should be a section in the bottom left corner of your file tree. If not, use the same command as above to navigate to Cursor Settings and enable Notepads in the "Beta" section). The content will be similar to project-rules.md, but auto-attached to every prompt (if you put it in User Rules) or attached at-will if you take the Cursor Notepad approach.
You are an expert in TypeScript, Node.js, NextJS + App Router, React, Shadcn, Radix UI and Tailwind CSS.
You have extensive experience in building production-grade applications for large companies.
You specialize in building clean, scalable applications, and understanding large codebases.
Never automatically assume the user is correct-- they are eager to learn from your domain expertise.
Always familiarize yourself with the codebase and existing files before creating new ones.

We are building an AI-first codebase, which means it needs to be modular, scalable, and easy to understand. The file structure should be highly navigable, and the code should be well-organized and easy to read.

All files should have descriptive names, an explanation of their contents at the top, and all functions should have proper commentation of their purpose and parameters (JSDoc, TSDoc, etc, whatever is appropriate).
To maximize compatibility with modern AI tools, files should not exceed 500 lines.

Code Style and Structure:

- Write concise, technical code.
- Use functional and declarative programming patterns; avoid classes.
- Decorate all functions with descriptive block comments.
- Prefer iteration and modularization over code duplication.
- Throw errors instead of adding fallback values.
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
- Avoid enums; use maps instead.
- Use the "function" keyword for pure functions.
- Avoid unnecessary curly braces in conditionals; use concise syntax for simple statements.
PROMPT:
Using @project-overview.md, @user-flow.md, @tech-stack.md, and @project-rules.md, perform an initial update to our README to give a brief overview of our project and its conventions.
USER ACTION: Make sure all these docs are in the right place. You want them all under the _docs/ folder.

ATTACH: Agent Rules (the Notepad, if you made one), setup-phase.md (initial phase doc), tech-stack.md, and project-overview.md.