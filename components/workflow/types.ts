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

export type StepExample =
  | { type: "code"; language?: string; code: string }
  | { type: "image"; src: string; alt: string }
  | { type: "quote"; text: string }

export type Step = {
  id: string
  intent: string
  action: string
  tool: { id: string; name: string; category?: string; icon?: IconName }
  example?: StepExample
  tip?: string
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
  steps: Step[]
  principles: string[]
  exampleOutputs?: ExampleOutput[]
  relatedBuilders?: RelatedBuilder[]
}
