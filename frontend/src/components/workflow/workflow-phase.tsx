/**
 * @fileoverview Large phase card with header bar, tools, and expandable practice sub-cards.
 */

"use client"

import { useState, useEffect, useRef } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { PracticeCard } from "@/components/workflow/practice-card"
import type { PhaseData, PhaseConfig } from "./types"

type WorkflowPhaseProps = {
  phase: PhaseData
  config: PhaseConfig
  expandedAll: boolean
  onInView?: (inView: boolean) => void
}

/**
 * @description Large rounded phase card with bold header and practice sub-cards.
 */
export function WorkflowPhase({ phase, config, expandedAll, onInView }: WorkflowPhaseProps) {
  const [isInView, setIsInView] = useState(false)
  const phaseRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        const inView = entry.isIntersecting
        setIsInView(inView)
        onInView?.(inView)
      },
      { threshold: 0.3, rootMargin: "-100px 0px -100px 0px" },
    )

    if (phaseRef.current) {
      observer.observe(phaseRef.current)
    }

    return () => observer.disconnect()
  }, [onInView])

  return (
    <Card ref={phaseRef} id={phase.id} className="border-zinc-200/70 bg-white shadow-sm overflow-hidden scroll-mt-32">
      {/* Bold Header Bar */}
      <div className="bg-gradient-to-r from-zinc-900 to-zinc-800 text-white p-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div className="min-w-0">
            <h3 className="text-xl font-bold tracking-tight">{phase.title}</h3>
            <p className="mt-1 text-zinc-200 text-sm leading-relaxed">{phase.summary}</p>
          </div>
          {phase.toolsUsed?.length ? (
            <div className="flex flex-wrap gap-2 md:max-w-xs">
              <span className="text-xs text-zinc-300 w-full md:w-auto">Tools:</span>
              {phase.toolsUsed.map((tool) => (
                <Badge key={tool} variant="secondary" className="bg-white/20 text-white border-white/30 text-xs">
                  {tool}
                </Badge>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      {/* Phase Content */}
      <div className="p-6">
        {phase.practices.length > 0 ? (
          <div className="space-y-4">
            {phase.practices.map((practice) => (
              <PracticeCard key={practice.id} practice={practice} expandedAll={expandedAll} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-zinc-500">
            <p className="text-sm">No specific practices documented for this phase yet.</p>
            <p className="text-xs mt-1 text-zinc-400">Check back as more content is added.</p>
          </div>
        )}
      </div>
    </Card>
  )
}
