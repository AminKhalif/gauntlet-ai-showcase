/**
 * @fileoverview Workflow profile page rendering AI-first sections with strong visual hierarchy.
 */

import { notFound } from "next/navigation"
import type { Metadata } from "next"
import { BuilderHeader } from "@/components/workflow/builder-header"
import { Principles } from "@/components/workflow/principles"
import { ExampleOutputs } from "@/components/workflow/example-outputs"
import { RelatedBuilders } from "@/components/workflow/related-builders"
import { PhaseCard } from "@/components/workflow/phase-card"
import { Separator } from "@/components/ui/separator"
import { WORKFLOWS, assertHasRequiredPhases } from "@/components/workflow/data"

export const metadata: Metadata = {
  title: "AI-first Workflow Showcase",
}

/**
 * @description Renders a single workflow profile by slug with strict validation and clear sectioning.
 */
export default function WorkflowPage({
  params,
}: {
  params: { slug: string }
}) {
  const slug = params?.slug
  const workflow = WORKFLOWS[slug]
  if (!workflow) {
    notFound()
  }

  assertHasRequiredPhases(workflow)

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

          <Separator className="my-10" />

          <section aria-labelledby="phases-heading" className="mt-4">
            <div className="mb-6">
              <h2 id="phases-heading" className="text-2xl md:text-3xl font-bold tracking-tight text-zinc-900">
                How They Build with AI
              </h2>
              <p className="mt-2 text-sm text-zinc-500">
                Organized into phases with practices, quotes, and artifacts for quick scanning and deep reading.
              </p>
            </div>

            <div className="space-y-6">
              {workflow.phases.map((phase) => (
                <PhaseCard key={phase.id} phase={phase} />
              ))}
            </div>
          </section>

          {workflow.principles?.length ? (
            <section aria-labelledby="principles-heading" className="mt-12">
              <h2 id="principles-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
                Principles & Patterns
              </h2>
              <p className="mt-2 text-sm text-zinc-500">Best practices guiding this workflow.</p>
              <Principles items={workflow.principles} />
            </section>
          ) : null}

          {workflow.exampleOutputs?.length ? (
            <section aria-labelledby="outputs-heading" className="mt-12">
              <h2 id="outputs-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
                Example Outputs
              </h2>
              <p className="mt-2 text-sm text-zinc-500">Optional screenshots, repositories, and demos.</p>
              <ExampleOutputs items={workflow.exampleOutputs} />
            </section>
          ) : null}

          {workflow.relatedBuilders?.length ? (
            <section aria-labelledby="related-heading" className="mt-12 mb-16">
              <h2 id="related-heading" className="text-lg font-semibold tracking-tight text-zinc-900">
                Related Builders
              </h2>
              <RelatedBuilders builders={workflow.relatedBuilders} />
            </section>
          ) : null}
        </div>
      </div>
    </main>
  )
}
