import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Code2, Lightbulb, Quote, ImageIcon } from "lucide-react"
import { iconMap, getCategoryColor, cn } from "./utils"
import type { Step, StepExample } from "./types"

function ExampleBlock({ example }: { example?: StepExample }) {
  if (!example) return null
  if (example.type === "code") {
    return (
      <div className="rounded-md border border-zinc-200 bg-zinc-50">
        <div className="flex items-center justify-between border-b border-zinc-200 px-3 py-2">
          <div className="flex items-center gap-2 text-xs text-zinc-600">
            <Code2 className="size-4" aria-hidden="true" />
            <span>{example.language?.toUpperCase() || "CODE"}</span>
          </div>
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
  return null
}

export function StepCard({
  step,
  index = 0,
}: {
  step: Step
  index?: number
}) {
  const Icon = step.tool.icon ? iconMap[step.tool.icon] : iconMap.Code2
  const color = getCategoryColor(step.tool.category || "")
  const number = index + 1

  return (
    <Card className="border-zinc-200/70 bg-white/70 p-4 md:p-6">
      <div className="flex items-start gap-3">
        <div
          className={cn(
            "mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-full text-sm font-medium ring-1",
            color,
          )}
          aria-label={`Step ${number}`}
          role="img"
        >
          {number}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="text-base md:text-lg font-semibold tracking-tight text-zinc-900">{step.intent}</h3>
            <Badge variant="secondary" className={cn("ring-1", color)}>
              <span className="inline-flex items-center gap-1">
                <Icon className="size-3.5" aria-hidden="true" />
                <span className="text-xs">{step.tool.name}</span>
              </span>
            </Badge>
          </div>

          <div className="mt-3 grid grid-cols-1 gap-4 md:grid-cols-5">
            <div className="md:col-span-2">
              <h4 className="text-sm font-medium text-zinc-800">Action</h4>
              <p className="mt-1 text-sm text-zinc-600">{step.action}</p>
            </div>
            <div className="md:col-span-3">
              <h4 className="text-sm font-medium text-zinc-800">Example</h4>
              <div className="mt-2">
                <ExampleBlock example={step.example} />
              </div>
            </div>
          </div>

          {step.tip ? (
            <div className="mt-4 rounded-md border border-emerald-200 bg-emerald-50/70 p-3">
              <div className="flex items-start gap-2">
                <Lightbulb className="mt-0.5 size-4 text-emerald-600" aria-hidden="true" />
                <div>
                  <h5 className="text-xs font-semibold uppercase tracking-wide text-emerald-700">Tip</h5>
                  <p className="mt-1 text-sm text-emerald-800">{step.tip}</p>
                </div>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </Card>
  )
}
