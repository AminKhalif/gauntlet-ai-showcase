import type React from "react"
/**
 * @fileoverview Generic section card for AI-first profile blocks with approach, examples, and tips.
 */

import { Card } from "@/components/ui/card"
import { Lightbulb, Code2, ImageIcon, Quote } from "lucide-react"
import { cn } from "./utils"
import type { ExampleBlock } from "./types"

type SectionCardProps = {
  title: string
  approach: string
  examples?: ExampleBlock[]
  tips?: string[]
  emphasize?: boolean
  children?: React.ReactNode
}

/**
 * @description Displays a labeled section with a primary approach paragraph and optional examples/tips.
 */
export function SectionCard({
  title,
  approach,
  examples = [],
  tips = [],
  emphasize = false,
  children,
}: SectionCardProps) {
  return (
    <Card
      className={cn(
        "border-zinc-200/70 bg-white/70 p-4 md:p-6",
        emphasize && "ring-1 ring-zinc-200 shadow-[0_1px_0_0_rgba(0,0,0,0.03)]",
      )}
    >
      <div className="flex flex-col gap-4">
        <header>
          <h3 className="text-base md:text-lg font-semibold tracking-tight text-zinc-900">{title}</h3>
        </header>

        <p className="text-sm text-zinc-700 leading-relaxed">{approach}</p>

        {children ? <div className="pt-1">{children}</div> : null}

        {examples.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {examples.map((example, index) => (
              <ExampleBlockView key={index} example={example} />
            ))}
          </div>
        ) : null}

        {tips.length > 0 ? (
          <div className="mt-1 grid grid-cols-1 gap-2">
            {tips.map((tip, index) => (
              <div
                key={index}
                className="rounded-md border border-emerald-200 bg-emerald-50/70 p-3 text-sm text-emerald-800"
              >
                <div className="flex items-start gap-2">
                  <Lightbulb className="mt-0.5 size-4 text-emerald-600" aria-hidden="true" />
                  <p>{tip}</p>
                </div>
              </div>
            ))}
          </div>
        ) : null}
      </div>
    </Card>
  )
}

/**
 * @description Renders a single example block (code, image, or quote).
 */
function ExampleBlockView({ example }: { example: ExampleBlock }) {
  if (example.type === "code") {
    return (
      <div className="rounded-md border border-zinc-200 bg-zinc-50">
        <div className="flex items-center gap-2 border-b border-zinc-200 px-3 py-2 text-xs text-zinc-600">
          <Code2 className="size-4" aria-hidden="true" />
          <span>{example.language?.toUpperCase() || "CODE"}</span>
        </div>
        <pre className="overflow-x-auto p-4 text-sm text-zinc-800">
          <code>{example.code}</code>
        </pre>
      </div>
    )
  }
  if (example.type === "image") {
    return (
      <figure className="overflow-hidden rounded-md border border-zinc-200">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={example.src || "/placeholder.svg"} alt={example.alt} className="h-auto w-full" />
        <figcaption className="flex items-center gap-2 border-t border-zinc-200 bg-white px-3 py-2 text-xs text-zinc-600">
          <ImageIcon className="size-4" aria-hidden="true" />
          <span>Example screenshot</span>
        </figcaption>
      </figure>
    )
  }
  if (example.type === "quote") {
    return (
      <blockquote className="rounded-md border border-zinc-200 bg-white p-4 text-zinc-700">
        <div className="mb-2 flex items-center gap-2 text-xs text-zinc-500">
          <Quote className="size-4" aria-hidden="true" />
          <span>Quote</span>
        </div>
        <p className="leading-relaxed">{example.text}</p>
      </blockquote>
    )
  }
  throw new Error("Unsupported example block type")
}
