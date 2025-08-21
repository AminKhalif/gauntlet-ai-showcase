/**
 * @fileoverview Sticky phase navigation bar with scrollspy highlighting.
 */

"use client"

import { Button } from "@/components/ui/button"
import type { PhaseConfig } from "./types"
import { cn } from "./utils"

type PhaseNavigationProps = {
  phases: PhaseConfig[]
  activePhase: string | null
  onPhaseClick: (phaseId: string) => void
}

/**
 * @description Sticky navigation bar for jumping between workflow phases with active highlighting.
 */
export function PhaseNavigation({ phases, activePhase, onPhaseClick }: PhaseNavigationProps) {
  return (
    <div className="sticky top-16 z-40 bg-white border-b border-zinc-200">
      <div className="mx-auto max-w-5xl px-4">
        <div className="flex items-center gap-1 overflow-x-auto py-3">
          {phases.map((phase) => (
            <Button
              key={phase.id}
              variant="ghost"
              size="sm"
              onClick={() => onPhaseClick(phase.id)}
              className={cn(
                "whitespace-nowrap text-sm font-medium transition-colors",
                activePhase === phase.id
                  ? "bg-zinc-900 text-white hover:bg-zinc-800"
                  : "text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100",
              )}
            >
              {phase.shortName || phase.title}
            </Button>
          ))}
        </div>
      </div>
    </div>
  )
}
