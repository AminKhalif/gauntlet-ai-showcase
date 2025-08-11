import type { Workflow } from "./types"

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
      "Jane practices an iterative prompting approach with tight feedback loops. She starts broad, narrows context using tool-aware prompts, and validates outputs with quick runnable examples. She optimizes for repeatability and code quality by embedding tests early.",
    tools: [
      {
        id: "gpt-4o",
        name: "GPT-4o",
        category: "Code Generation",
        purpose: "Drafts functions and refactors based on specs",
        icon: "Bot",
      },
      {
        id: "cursor",
        name: "Cursor",
        category: "IDE Assistant",
        purpose: "In-editor context, diffing, and inline explain/fix",
        icon: "SquareTerminal",
      },
      {
        id: "copilot",
        name: "GitHub Copilot",
        category: "Code Completion",
        purpose: "Fills small gaps and suggests boilerplate",
        icon: "Sparkles",
      },
      {
        id: "jest",
        name: "Jest",
        category: "Testing",
        purpose: "Validates generated code with unit tests",
        icon: "FlaskConical",
      },
      {
        id: "postman",
        name: "Postman",
        category: "API Debugging",
        purpose: "Quickly probes endpoints and verifies payloads",
        icon: "Network",
      },
      {
        id: "langchain",
        name: "LangChain",
        category: "Tool Chaining",
        purpose: "Orchestrates tools for repeatable runs",
        icon: "Workflow",
      },
    ],
    principles: [
      "iterative prompting",
      "tool chaining",
      "tight feedback loops",
      "spec-first thinking",
      "guardrails with tests",
      "context minimization",
    ],
    steps: [
      {
        id: "step-1",
        intent: "Clarify requirements and constraints",
        action:
          "Write a crisp spec with inputs, outputs, and edge cases. Ask the model to restate understanding and propose a minimal plan.",
        tool: { id: "gpt-4o", name: "GPT-4o", icon: "Bot", category: "Code Generation" },
        example: {
          type: "quote",
          text: "Summarize goals as bullet points and propose 3-5 checkpoints we can verify with tests.",
        },
        tip: "Keep the spec under 150 words to reduce prompt drift.",
      },
      {
        id: "step-2",
        intent: "Draft the core function",
        action: "Generate the smallest working function guided by the spec. Avoid frameworks. Keep pure and testable.",
        tool: { id: "cursor", name: "Cursor", icon: "SquareTerminal", category: "IDE Assistant" },
        example: {
          type: "code",
          language: "ts",
          code: `export function slugify(input: string): string {
  return input
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\\u0300-\\u036f]/g, "")
    .replace(/[^a-z0-9\\s-]/g, "")
    .trim()
    .replace(/[\\s-]+/g, "-");
}`,
        },
        tip: "Ask for 2-3 alternative implementations and diff them.",
      },
      {
        id: "step-3",
        intent: "Add tests and run quick feedback loop",
        action: "Generate unit tests capturing edge cases; run and fix. Treat failing tests as prompts.",
        tool: { id: "jest", name: "Jest", icon: "FlaskConical", category: "Testing" },
        example: {
          type: "code",
          language: "ts",
          code: `import { slugify } from "./slugify";
test("handles diacritics", () => {
  expect(slugify("Crème Brûlée")).toBe("creme-brulee");
});
test("collapses whitespace", () => {
  expect(slugify("  Hello   World ")).toBe("hello-world");
});`,
        },
      },
      {
        id: "step-4",
        intent: "Integrate and validate via API probes",
        action: "Expose the function in a minimal handler and verify with Postman collections.",
        tool: { id: "postman", name: "Postman", icon: "Network", category: "API Debugging" },
        example: {
          type: "image",
          src: "/placeholder.svg?height=320&width=560",
          alt: "Postman verifying slugify endpoint",
        },
        tip: "Cache representative requests to replay quickly after refactors.",
      },
      {
        id: "step-5",
        intent: "Orchestrate repeatable runs",
        action: "Wire tools with LangChain for testable, deterministic flows where possible.",
        tool: { id: "langchain", name: "LangChain", icon: "Workflow", category: "Tool Chaining" },
        example: { type: "quote", text: "Make the happy path one command; make the edge cases easy to replay." },
      },
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
