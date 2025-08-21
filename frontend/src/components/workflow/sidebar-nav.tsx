/**
 * @fileoverview Sticky sidebar navigation for quick phase jumping with visual indicators.
 */

"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import type { PhaseConfig, Workflow } from "./types"
import { cn } from "./utils"

type SidebarNavProps = {
  phases: PhaseConfig[]
  activePhase: string | null
  onPhaseClick: (phaseId: string) => void
  workflow: Workflow
}

/**
 * @description Sticky sidebar with phase navigation and builder info.
 */
export function SidebarNav({ phases, activePhase, onPhaseClick, workflow }: SidebarNavProps) {
  const initials = workflow.builder.name
    .split(" ")
    .map((s) => s[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="fixed left-0 top-0 h-screen w-80 bg-white/80 backdrop-blur border-r border-zinc-200/50 overflow-y-auto">
      <div className="p-6">
        {/* Builder Mini Profile */}
        <Card className="p-4 mb-6 bg-gradient-to-r from-zinc-900 to-zinc-800 text-white">
          <div className="flex items-center gap-3">
            <Avatar className="size-12 ring-2 ring-white/20">
              <AvatarImage
                src={workflow.builder.avatar || "/placeholder.svg?height=96&width=96&query=builder-avatar"}
                alt={`${workflow.builder.name} avatar`}
              />
              <AvatarFallback className="bg-white/20 text-white">{initials}</AvatarFallback>
            </Avatar>
            <div className="min-w-0">
              <h3 className="font-semibold truncate">{workflow.builder.name}</h3>
              <p className="text-sm text-zinc-300 truncate">{workflow.builder.role}</p>
            </div>
          </div>
        </Card>

        {/* Phase Navigation */}
        <nav aria-label="Workflow phases">
          <h4 className="text-sm font-semibold text-zinc-900 mb-4 uppercase tracking-wide">Workflow Phases</h4>
          <ul className="space-y-2">
            {phases.map((phase) => {
              const phaseData = workflow.phases.find((p) => p.id === phase.id)
              const isActive = activePhase === phase.id
              const practiceCount = phaseData?.practices.length || 0

              return (
                <li key={phase.id}>
                  <button
                    onClick={() => onPhaseClick(phase.id)}
                    className={cn(
                      "w-full text-left p-3 rounded-lg transition-all duration-200 group",
                      isActive
                        ? "bg-zinc-900 text-white shadow-lg"
                        : "hover:bg-zinc-100 text-zinc-700 hover:text-zinc-900",
                    )}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-sm">{phase.shortName || phase.title}</span>
                      {practiceCount > 0 && (
                        <Badge
                          variant="secondary"
                          className={cn("text-xs", isActive ? "bg-white/20 text-white" : "bg-zinc-200 text-zinc-600")}
                        >
                          {practiceCount}
                        </Badge>
                      )}
                    </div>
                    <p
                      className={cn(
                        "text-xs leading-relaxed",
                        isActive ? "text-zinc-300" : "text-zinc-500 group-hover:text-zinc-600",
                      )}
                    >
                      {phase.description}
                    </p>
                    {phaseData?.toolsUsed && phaseData.toolsUsed.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {phaseData.toolsUsed.slice(0, 3).map((tool) => (
                          <span
                            key={tool}
                            className={cn(
                              "text-xs px-2 py-0.5 rounded-full",
                              isActive
                                ? "bg-white/10 text-zinc-200"
                                : "bg-zinc-100 text-zinc-600 group-hover:bg-zinc-200",
                            )}
                          >
                            {tool}
                          </span>
                        ))}
                        {phaseData.toolsUsed.length > 3 && (
                          <span
                            className={cn(
                              "text-xs",
                              isActive ? "text-zinc-400" : "text-zinc-500 group-hover:text-zinc-600",
                            )}
                          >
                            +{phaseData.toolsUsed.length - 3}
                          </span>
                        )}
                      </div>
                    )}
                  </button>
                </li>
              )
            })}
          </ul>
        </nav>
      </div>
    </div>
  )
}
