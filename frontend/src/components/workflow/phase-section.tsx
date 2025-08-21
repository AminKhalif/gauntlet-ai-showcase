/**
 * @fileoverview Clean phase section with tools header and expandable practice cards.
 */

"use client"

import { cn } from "@/lib/utils"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { PracticeCard } from "@/components/workflow/practice-card"
import { ChevronDown, ChevronUp } from "lucide-react"
import type { PhaseData, PhaseConfig, Workflow } from "./types"

type PhaseSectionProps = {
  phase: PhaseData
  config: PhaseConfig
  workflow: Workflow
}

/**
 * @description Clean phase section with tools header and collapsible practice cards.
 */
export function PhaseSection({ phase, config, workflow }: PhaseSectionProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <section id={phase.id} className="scroll-mt-32">
      <Card className="border-zinc-200 bg-white shadow-sm">
        {/* Phase Header */}
        <div className="p-6 border-b border-zinc-100">
          <div className="flex items-start justify-between gap-6">
            <div className="flex-1">
              <h2 className="text-xl font-bold text-zinc-900 mb-2">{phase.title}</h2>
              <p className="text-zinc-600 leading-relaxed">{phase.summary}</p>
            </div>

            {/* Tools Used */}
            {phase.toolsUsed?.length ? (
              <div className="shrink-0">
                <div className="text-sm font-medium text-zinc-600 mb-2">Tools used</div>
                <div className="flex flex-wrap gap-2 max-w-xs">
                  {phase.toolsUsed.map((toolName) => {
                    const tool = workflow.tools.find((t) => t.name === toolName)
                    return (
                      <Badge
                        key={toolName}
                        variant="outline"
                        className="bg-zinc-50 border-zinc-300 text-zinc-700 hover:bg-zinc-100 transition-colors cursor-help"
                        title={tool?.purpose || `${toolName} usage in this phase`}
                      >
                        {toolName}
                      </Badge>
                    )
                  })}
                </div>
              </div>
            ) : null}
          </div>

          {/* Expand/Collapse Controls */}
          {phase.practices.length > 0 && (
            <div className="mt-4 flex items-center justify-between">
              <span className="text-sm text-zinc-500">
                {phase.practices.length} {phase.practices.length === 1 ? "practice" : "practices"}
              </span>
              <Button variant="ghost" size="sm" onClick={toggleExpanded} className="text-zinc-600 hover:text-zinc-900">
                {isExpanded ? (
                  <>
                    <ChevronUp className="size-4 mr-1" />
                    Collapse all
                  </>
                ) : (
                  <>
                    <ChevronDown className="size-4 mr-1" />
                    Expand all
                  </>
                )}
              </Button>
            </div>
          )}
        </div>

        {/* Practice Cards */}
        {phase.practices.length > 0 ? (
          <div
            className={cn(
              "transition-all duration-300 ease-in-out overflow-hidden",
              isExpanded ? "max-h-none opacity-100" : "max-h-0 opacity-0",
            )}
          >
            <div className="p-6 space-y-4">
              {phase.practices.map((practice) => (
                <PracticeCard key={practice.id} practice={practice} workflow={workflow} />
              ))}
            </div>
          </div>
        ) : (
          <div className="p-6 text-center text-zinc-500">
            <p className="text-sm">No practices documented for this phase yet.</p>
          </div>
        )}
      </Card>
    </section>
  )
}
