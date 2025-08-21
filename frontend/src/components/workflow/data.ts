/**
 * @fileoverview Enhanced workflow data with all required phases and validation.
 */

import type { SectionName, Workflow, PhaseConfig } from "./types"

/**
 * @description Required phases that must always be rendered in exact order.
 */
export const REQUIRED_PHASES: PhaseConfig[] = [
  {
    id: "planning-scoping",
    title: "Planning & Scoping",
    shortName: "Planning",
    description: "Define clear requirements and constraints before any code generation.",
    required: true,
  },
  {
    id: "context-management",
    title: "Context Management",
    shortName: "Context",
    description: "Structure prompts and manage information flow to AI tools.",
    required: true,
  },
  {
    id: "codegen-loop",
    title: "Codegen Loop",
    shortName: "Codegen",
    description: "Generate, review, and iterate on code with AI assistance.",
    required: true,
  },
  {
    id: "verification-safeguards",
    title: "Verification & Safeguards",
    shortName: "Verification",
    description: "Ensure correctness, reliability, and quality through testing and validation.",
    required: true,
  },
  {
    id: "iteration-style",
    title: "Iteration Style",
    shortName: "Iteration",
    description: "Refine and evolve work through feedback cycles.",
    required: true,
  },
  {
    id: "deployment-delivery",
    title: "Deployment & Delivery",
    shortName: "Deploy",
    description: "Ship and deliver the final product or solution.",
    required: true,
  },
]

/**
 * @description Canonical order for AI-first profile sections.
 */
export const SECTION_ORDER: SectionName[] = [
  "Planning & Scoping",
  "Context Management",
  "Guardrails & Validation",
  "Iteration Style",
  "Tool Stack",
  "Integration & Orchestration",
  "Deployment & Delivery",
]

/**
 * @description Validates that all required phases are present in workflow.
 */
export function assertHasAllPhases(workflow: Workflow): void {
  const requiredPhaseIds = REQUIRED_PHASES.filter((p) => p.required).map((p) => p.id)
  const presentPhaseIds = workflow.phases.map((p) => p.id)
  const missing = requiredPhaseIds.filter((id) => !presentPhaseIds.includes(id))

  if (missing.length > 0) {
    console.warn(
      `Workflow "${workflow.slug}" is missing required phases: ${missing.join(", ")}. Mock content will be used.`,
    )
  }
}

/**
 * @description Enhanced demo data with all required phases and realistic content.
 */
export const WORKFLOWS: Record<string, Workflow> = {
  "jane-iterative-builder": {
    slug: "jane-iterative-builder",
    builder: {
      name: "Jane Cooper",
      role: "AI Software Engineer",
      avatar: "/placeholder.svg?height=128&width=128",
      sourceUrl: "https://example.com/jane-workflow",
    },
    summary:
      "Jane builds with tight iteration loops, spec-first thinking, and explicit guardrails. She prefers minimal prompts, code-level validation, and repeatable orchestration for reliability at scale.",
    tools: [
      {
        id: "gpt-4o",
        name: "GPT-4o",
        category: "Code Generation",
        purpose: "Drafts and refactors code to match specifications",
        icon: "Bot",
      },
      {
        id: "cursor",
        name: "Cursor",
        category: "IDE Assistant",
        purpose: "Context-aware edits, diffs, and inline explanations",
        icon: "SquareTerminal",
      },
      {
        id: "copilot",
        name: "GitHub Copilot",
        category: "Code Completion",
        purpose: "Fills boilerplate and small glue code gaps",
        icon: "Sparkles",
      },
      {
        id: "jest",
        name: "Jest",
        category: "Testing",
        purpose: "Runs unit tests as validation guardrails",
        icon: "FlaskConical",
      },
      {
        id: "postman",
        name: "Postman",
        category: "API Debugging",
        purpose: "Verifies endpoints and payload structures",
        icon: "Network",
      },
      {
        id: "langchain",
        name: "LangChain",
        category: "Tool Chaining",
        purpose: "Orchestrates deterministic and replayable flows",
        icon: "Workflow",
      },
    ],
    phases: [
      {
        id: "planning-scoping",
        title: "Planning & Scoping",
        summary: "Define clear requirements and constraints before any code generation.",
        toolsUsed: ["GPT-4o", "Cursor"],
        practices: [
          {
            id: "spec-first",
            type: "Rule",
            title: "Write specs under 150 words",
            explanation:
              "Define inputs, outputs, and edge cases clearly. Ask the model to restate understanding and propose 3-5 testable checkpoints. Use bullet points over paragraphs for clarity and precision.",
            quotes: [
              {
                id: "q1",
                text: "I always start with a crisp spec. If I can't explain it in 150 words, the problem isn't clear enough yet.",
                timestamp: "00:02:15",
                speaker: "Jane",
              },
              {
                id: "q2",
                text: "The model should restate my requirements back to me. If it gets something wrong, I know my spec was ambiguous.",
                timestamp: "00:02:45",
                speaker: "Jane",
              },
            ],
            artifacts: ["spec-template.md", "requirements-checklist.json", "acceptance-criteria.yml"],
          },
        ],
      },
      {
        id: "context-management",
        title: "Context Management",
        summary: "Structure prompts and manage information flow to AI tools.",
        toolsUsed: ["Cursor", "GPT-4o"],
        practices: [
          {
            id: "minimal-context",
            type: "Rule",
            title: "Reference one file at a time",
            explanation:
              "Avoid dumping entire repositories. Use editor tools to highlight specific functions or classes. Link targeted snippets rather than raw paste. Keep context under 50 lines when possible.",
            quotes: [
              {
                id: "q4",
                text: "I never paste more than 50 lines at once. The model gets confused with too much context.",
                timestamp: "00:05:10",
                speaker: "Jane",
              },
            ],
            artifacts: ["context-template.md", "diff-examples/"],
          },
        ],
      },
      {
        id: "codegen-loop",
        title: "Codegen Loop",
        summary: "Generate, review, and iterate on code with AI assistance.",
        toolsUsed: ["GPT-4o", "Cursor", "GitHub Copilot"],
        practices: [
          {
            id: "smallest-working-version",
            type: "Rule",
            title: "Start with the smallest working function",
            explanation:
              "Generate the minimal viable implementation first. Avoid frameworks and dependencies initially. Focus on pure functions that can be easily tested and understood.",
            quotes: [
              {
                id: "q6",
                text: "I always ask for the simplest version first. You can add complexity later, but you can't easily remove it.",
                timestamp: "00:07:20",
                speaker: "Jane",
              },
            ],
            artifacts: ["minimal-function.ts", "complexity-progression.md"],
          },
        ],
      },
      {
        id: "verification-safeguards",
        title: "Verification & Safeguards",
        summary: "Ensure correctness, reliability, and quality through testing and validation.",
        toolsUsed: ["Jest", "Postman"],
        practices: [
          {
            id: "test-driven-feedback",
            type: "Rule",
            title: "Treat failing tests as prompts",
            explanation:
              "Generate tests from the spec immediately. Run them against the generated code. Use test failures as specific, actionable feedback for the next iteration. This creates a tight feedback loop.",
            quotes: [
              {
                id: "q8",
                text: "A failing test is the best prompt you can give an AI. It's specific, actionable, and unambiguous.",
                timestamp: "00:10:15",
                speaker: "Jane",
              },
            ],
            artifacts: ["test-suite.spec.ts", "failure-logs.txt"],
          },
        ],
      },
      {
        id: "iteration-style",
        title: "Iteration Style",
        summary: "Refine and evolve work through feedback cycles.",
        toolsUsed: ["Jest", "Postman"],
        practices: [
          {
            id: "small-iterations",
            type: "Practice",
            title: "Make 10 small improvements over 1 big leap",
            explanation:
              "Build in small, verifiable increments. Each step should be testable and reversible. Prefer many small iterations over few large ones. Use concrete feedback mechanisms like tests, demos, or user validation.",
            quotes: [
              {
                id: "q10",
                text: "Small iterations compound. Big iterations usually fail. I'd rather make 10 small improvements than attempt one big leap.",
                timestamp: "00:14:20",
                speaker: "Jane",
              },
            ],
            artifacts: ["iteration-log.md", "feedback-mechanisms.json"],
          },
        ],
      },
      {
        id: "deployment-delivery",
        title: "Deployment & Delivery",
        summary: "Ship and deliver the final product or solution.",
        toolsUsed: ["GitHub Actions", "Vercel"],
        practices: [
          {
            id: "minimal-demo-first",
            type: "Practice",
            title: "Ship a minimal demo immediately",
            explanation:
              "Create the smallest possible working demo as soon as you have a functioning core. This validates the approach early and provides a foundation for iteration and feedback.",
            quotes: [
              {
                id: "q9",
                text: "I deploy a basic demo within the first hour. It doesn't have to be pretty, it just has to work.",
                timestamp: "00:12:30",
                speaker: "Jane",
              },
            ],
            artifacts: ["demo-app/", "deployment-config.yml"],
          },
        ],
      },
    ],
    sections: {
      "Planning & Scoping": {
        approach:
          "Write a crisp spec under 150 words: inputs, outputs, constraints, edge cases. Ask the model to restate understanding and propose a minimal plan. Prefer bullet points and acceptance checks.",
        examples: [
          {
            type: "quote",
            text: "Summarize goals and propose 3–5 checkpoints we can verify with tests.",
          },
        ],
        tips: ["Use concrete examples over abstract requirements", "Define success and failure explicitly"],
      },
      "Context Management": {
        approach:
          "Minimize prompt context. Reference the spec and one focused file at a time. Use editor-native tools to highlight diffs for the model. Avoid dumping large repos; link targeted snippets.",
        examples: [
          {
            type: "code",
            language: "ts",
            code: `/** Spec: slugify utility (inputs, outputs, edge cases) */
export function slugify(input: string): string {
  return input
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\\u0300-\\u036f]/g, "")
    .replace(/[^a-z0-9\\s-]/g, "")
    .trim()
    .replace(/[\\s-]+/g, "-");
}`,
          },
        ],
        tips: ["Prefer linked snippets over raw paste", "Keep prompts stable; change code, not the spec"],
      },
      "Guardrails & Validation": {
        approach:
          "Generate tests from the spec, run them immediately, and treat failing tests as prompts. For APIs, add Postman checks. Pin versions and surface errors loudly.",
        examples: [
          {
            type: "code",
            language: "ts",
            code: `import { slugify } from "./slugify";
test("handles diacritics", () => {
  expect(slugify("Crème Brûlée")).toBe("creme-brulee");
});`,
          },
          {
            type: "image",
            src: "/placeholder.svg?height=280&width=500",
            alt: "Postman verification of API responses",
          },
        ],
        tips: ["Fail fast; never ignore thrown errors", "Add minimal but meaningful coverage"],
      },
      "Iteration Style": {
        approach:
          "Start with the smallest working version and iterate in diffs. Ask for alternative implementations and compare tradeoffs. Keep commits focused and reversible.",
        examples: [
          {
            type: "quote",
            text: "Make the happy path one command; replay edge cases in seconds.",
          },
        ],
        tips: ["Commit after each passing test cycle", "Prefer small PRs with precise scope"],
      },
      "Tool Stack": {
        approach:
          "Pair a general LLM with an IDE assistant, a completion engine, and a test runner. Add API probing and an orchestration layer only when needed.",
        tips: ["Favor tools that integrate into your editor and CI", "Automate checks early to prevent regressions"],
      },
      "Integration & Orchestration": {
        approach:
          "Expose small, testable surfaces (functions, routes). Use an orchestration layer for deterministic flows and caching. Keep interfaces typed and explicit.",
        examples: [
          {
            type: "quote",
            text: "Keep orchestration simple and transparent—log inputs/outputs for each tool call.",
          },
        ],
      },
      "Deployment & Delivery": {
        approach:
          "Ship a minimal demo first. Add CI to run tests and basic E2E checks. Provide a README and reproducible steps for reviewers.",
        examples: [
          {
            type: "image",
            src: "/placeholder.svg?height=300&width=640",
            alt: "Lightweight demo UI screenshot",
          },
        ],
        tips: ["Document assumptions and limits", "Automate smoke tests in CI"],
      },
    },
    principles: [
      "iterative prompting",
      "tool chaining",
      "tight feedback loops",
      "spec-first thinking",
      "guardrails with tests",
      "context minimization",
    ],
    exampleOutputs: [
      {
        type: "image",
        src: "/placeholder.svg?height=420&width=720",
        alt: "Demo UI screenshot",
        title: "Mini demo UI",
      },
      {
        type: "link",
        url: "https://github.com/example/slugify-ai-demo",
        label: "GitHub Repository",
        title: "Slugify AI Demo Repo",
      },
    ],
    relatedBuilders: [
      {
        name: "Devon Lane",
        role: "Full-stack with AI",
        avatar: "/placeholder.svg?height=96&width=96",
        shared: ["iterative prompting", "guardrails with tests"],
      },
      {
        name: "Arlene McCoy",
        role: "Data + LLM Ops",
        avatar: "/placeholder.svg?height=96&width=96",
        shared: ["tool chaining", "tight feedback loops"],
      },
      {
        name: "Courtney Henry",
        role: "DX/Tooling",
        avatar: "/placeholder.svg?height=96&width=96",
        shared: ["context minimization"],
      },
    ],
  },
}
