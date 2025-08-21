/**
 * @fileoverview Enhanced type definitions with required phase configuration and builder structure.
 */

import type { IconName } from "./utils"

export type Builder = {
  name: string
  role: string
  avatar: string
  sourceUrl?: string
}

export type Tool = {
  id: string
  name: string
  category: string
  purpose: string
  icon?: IconName
}

export type QuoteData = {
  id: string
  text: string
  timestamp: string
  speaker?: string
}

export type PracticeData = {
  id: string
  type: "Rule" | "Practice"
  title: string
  explanation: string
  quotes: QuoteData[]
  artifacts: string[]
}

export type PhaseData = {
  id: string
  title: string
  summary: string
  toolsUsed: string[]
  practices: PracticeData[]
}

export type PhaseConfig = {
  id: string
  title: string
  shortName?: string
  description: string
  required: boolean
}

export type ExampleBlock =
  | { type: "code"; language?: string; code: string }
  | { type: "image"; src: string; alt: string }
  | { type: "quote"; text: string }

export type SectionName =
  | "Planning & Scoping"
  | "Context Management"
  | "Guardrails & Validation"
  | "Iteration Style"
  | "Tool Stack"
  | "Integration & Orchestration"
  | "Deployment & Delivery"

export type SectionContent = {
  approach: string
  examples?: ExampleBlock[]
  tips?: string[]
}

export type ExampleOutput =
  | { type: "image"; src: string; alt: string; title?: string }
  | { type: "link"; url: string; label: string; title?: string }

export type RelatedBuilder = {
  name: string
  role: string
  avatar: string
  shared?: string[]
}

export type Workflow = {
  slug: string
  builder: Builder
  summary: string
  tools: Tool[]
  phases: PhaseData[]
  sections: Record<SectionName, SectionContent>
  principles: string[]
  exampleOutputs?: ExampleOutput[]
  relatedBuilders?: RelatedBuilder[]
}

// Legacy types for backward compatibility
export type StepExample =
  | { type: "code"; language?: string; code: string }
  | { type: "image"; src: string; alt: string }
  | { type: "quote"; text: string }

export type Step = {
  intent: string
  tool: {
    id: string
    name: string
    category: string
    icon?: IconName
  }
  action: string
  example?: StepExample
  tip?: string
}
