/**
 * @fileoverview Redesigned builder page with clean SaaS styling and sticky phase navigation.
 */

"use client"

import { useState, useEffect } from "react"
import { BuilderHeader } from "@/components/workflow/builder-header"
import { PhaseNavigation } from "@/components/workflow/phase-navigation"
import { PhaseSection } from "@/components/workflow/phase-section"
import { REQUIRED_PHASES, assertHasAllPhases, type Workflow } from "@/components/workflow/data"

/**
 * @description Clean, scannable builder profile with sticky navigation and distinct phase sections.
 */
export default function BuilderPageClient({
  builderId,
  workflow,
}: {
  builderId: string
  workflow: Workflow
}) {
  const [activePhase, setActivePhase] = useState<string | null>(null)

  assertHasAllPhases(workflow)

  const scrollToPhase = (phaseId: string) => {
    const element = document.getElementById(phaseId)
    if (element) {
      const offset = 120 // Account for sticky headers
      const elementPosition = element.getBoundingClientRect().top + window.pageYOffset
      window.scrollTo({
        top: elementPosition - offset,
        behavior: "smooth",
      })
    }
  }

  // Track active phase on scroll
  useEffect(() => {
    const handleScroll = () => {
      const phaseElements = REQUIRED_PHASES.map((phase) => ({
        id: phase.id,
        element: document.getElementById(phase.id),
      })).filter((item) => item.element)

      const scrollPosition = window.scrollY + 200

      for (let i = phaseElements.length - 1; i >= 0; i--) {
        const { id, element } = phaseElements[i]
        if (element && element.offsetTop <= scrollPosition) {
          setActivePhase(id)
          break
        }
      }
    }

    window.addEventListener("scroll", handleScroll)
    handleScroll() // Set initial active phase

    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-zinc-50">
      {/* Sticky Phase Navigation */}
      <PhaseNavigation phases={REQUIRED_PHASES} activePhase={activePhase} onPhaseClick={scrollToPhase} />

      <div className="mx-auto max-w-5xl px-4 py-8">
        <BuilderHeader builder={workflow.builder} />

        {/* Workflow Overview */}
        <section className="mt-12 mb-16">
          <h2 className="text-2xl font-bold text-zinc-900 mb-4">Workflow Overview</h2>
          <p className="text-lg text-zinc-700 leading-relaxed max-w-4xl">{workflow.summary}</p>
        </section>

        {/* Phase Sections */}
        <div className="space-y-12">
          {REQUIRED_PHASES.map((phaseConfig) => {
            const phaseData = workflow.phases.find((p) => p.id === phaseConfig.id) || {
              id: phaseConfig.id,
              title: phaseConfig.title,
              summary: phaseConfig.description,
              toolsUsed: [],
              practices: [],
            }

            return <PhaseSection key={phaseConfig.id} phase={phaseData} config={phaseConfig} workflow={workflow} />
          })}
        </div>
      </div>
    </div>
  )
}
