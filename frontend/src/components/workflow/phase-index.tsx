/**
 * @fileoverview Sticky phase navigation index for quick jumping between workflow sections.
 */

"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import type { PhaseConfig } from "./types"
import { cn } from "./utils"

type PhaseIndexProps = {
  phases: PhaseConfig[]
  activePhase: string | null
  onPhaseClick: (phaseId: string) => void
}

/**
 * @description Sticky navigation showing all phases with active state and smooth scrolling.
 */
export function PhaseIndex({ phases, activePhase, onPhaseClick }: PhaseIndexProps) {
  return (
    <div className="sticky top-20 z-40 bg-zinc-50/80 backdrop-blur border-b border-zinc-200/50">
      <div className="mx-auto max-w-5xl px-4 py-3">
        <Card className="border-zinc-200/70 bg-white/80 p-2">
          <div className="flex items-center gap-1 overflow-x-auto">
            <span className="text-xs font-medium text-zinc-500 whitespace-nowrap mr-2">Jump to:</span>
            {phases.map((phase) => (
              <Button
                key={phase.id}
                variant="ghost"
                size="sm"
                onClick={() => onPhaseClick(phase.id)}
                className={cn(
                  "text-xs whitespace-nowrap transition-colors",
                  activePhase === phase.id
                    ? "bg-zinc-900 text-white hover:bg-zinc-800"
                    : "text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100",
                )}
              >
                {phase.shortName || phase.title}
              </Button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
