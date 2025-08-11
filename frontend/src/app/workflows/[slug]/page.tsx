import { notFound } from "next/navigation"
import type { Metadata } from "next"
import { BuilderHeader } from "@/components/workflow/builder-header"
import { ToolsList } from "@/components/workflow/tools-list"
import { Principles } from "@/components/workflow/principles"
import { ExampleOutputs } from "@/components/workflow/example-outputs"
import { RelatedBuilders } from "@/components/workflow/related-builders"
import { StepCard } from "@/components/workflow/step-card"
import { Separator } from "@/components/ui/separator"
import { WORKFLOWS } from "@/components/workflow/data"

export const metadata: Metadata = {
  title: "AI Workflow Showcase",
}

export default function WorkflowPage({
  params,
}: {
  params: { slug: string }
}) {
  const workflow = WORKFLOWS[params.slug] || WORKFLOWS["jane-iterative-builder"]
  if (!workflow) notFound()

  return (
    <main className="min-h-screen bg-zinc-50">
      <div className="relative isolate">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-x-0 top-0 h-56 bg-gradient-to-b from-zinc-100 to-transparent"
        />
        <div className="mx-auto max-w-6xl px-4 py-8 md:py-12">
          <BuilderHeader builder={workflow.builder} />

          <section aria-labelledby="summary-heading" className="mt-8">
            <h2 id="summary-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
              Workflow Summary
            </h2>
            <p className="mt-3 text-zinc-600 leading-relaxed">{workflow.summary}</p>
          </section>

          <section aria-labelledby="tools-heading" className="mt-10">
            <div className="flex items-baseline justify-between gap-4">
              <h2 id="tools-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
                Tools Used
              </h2>
            </div>
            <ToolsList tools={workflow.tools} />
          </section>

          <Separator className="my-10" />

          <section aria-labelledby="steps-heading" className="mt-4">
            <div className="mb-6">
              <h2 id="steps-heading" className="text-2xl md:text-3xl font-bold tracking-tight text-zinc-900">
                Step-by-Step Workflow
              </h2>
              <p className="mt-2 text-sm text-zinc-500">
                The core of this showcase. Scan quickly or dive into examples and tips.
              </p>
            </div>

            <div className="space-y-6">
              {workflow.steps.map((step, idx) => (
                <StepCard key={step.id} step={step} index={idx} />
              ))}
            </div>
          </section>

          <section aria-labelledby="principles-heading" className="mt-12">
            <h2 id="principles-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
              Principles & Patterns
            </h2>
            <p className="mt-2 text-sm text-zinc-500">Best practices and strategies guiding this workflow.</p>
            <Principles items={workflow.principles} />
          </section>

          <section aria-labelledby="outputs-heading" className="mt-12">
            <h2 id="outputs-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
              Example Outputs
            </h2>
            <p className="mt-2 text-sm text-zinc-500">Optional screenshots, repositories, and demos.</p>
            <ExampleOutputs items={workflow.exampleOutputs} />
          </section>

          <section aria-labelledby="related-heading" className="mt-12 mb-16">
            <h2 id="related-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
              Related Builders
            </h2>
            <RelatedBuilders builders={workflow.relatedBuilders} />
          </section>
        </div>
      </div>
    </main>
  )
}
