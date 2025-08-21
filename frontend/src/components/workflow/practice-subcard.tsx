/**
 * @fileoverview Individual practice subcard with prominent explanations and subtle quotes.
 */

"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ChevronDown, ChevronUp, Code2, Copy, Play } from "lucide-react"
import type { PracticeData, Workflow } from "./types"
import { cn } from "./utils"

type PracticeSubcardProps = {
  practice: PracticeData
  expandedAll: boolean
  workflow: Workflow
}

/**
 * @description Individual practice card with structured content hierarchy and smooth animations.
 */
export function PracticeSubcard({ practice, expandedAll, workflow }: PracticeSubcardProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [showArtifacts, setShowArtifacts] = useState(false)

  useEffect(() => {
    setIsExpanded(expandedAll)
  }, [expandedAll])

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded)
  }

  const toggleArtifacts = () => {
    setShowArtifacts(!showArtifacts)
  }

  const typeColors = {
    Rule: "bg-red-50 text-red-700 border-red-200 ring-red-100",
    Practice: "bg-blue-50 text-blue-700 border-blue-200 ring-blue-100",
    Method: "bg-emerald-50 text-emerald-700 border-emerald-200 ring-emerald-100",
  }

  const typeColor = typeColors[practice.type as keyof typeof typeColors] || typeColors.Practice

  // Get tools mentioned in this practice
  const practiceTools = workflow.tools.filter(
    (tool) =>
      practice.explanation.toLowerCase().includes(tool.name.toLowerCase()) ||
      practice.quotes.some((quote) => quote.text.toLowerCase().includes(tool.name.toLowerCase())),
  )

  return (
    <Card className="bg-white/90 backdrop-blur border-zinc-200/70 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden">
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <Badge className={cn("text-xs px-3 py-1 border ring-1", typeColor)}>{practice.type}</Badge>
            <h3 className="text-xl font-semibold text-zinc-900 truncate">{practice.title}</h3>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleExpanded}
            className="shrink-0 text-zinc-500 hover:text-zinc-700 hover:bg-zinc-100 transition-colors"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="size-4 mr-1" />
                <span className="text-sm">Collapse</span>
              </>
            ) : (
              <>
                <ChevronDown className="size-4 mr-1" />
                <span className="text-sm">Expand</span>
              </>
            )}
          </Button>
        </div>

        {/* Explanation - Primary Content */}
        <div className="prose prose-zinc max-w-none">
          <div className="text-base text-zinc-800 leading-relaxed font-medium">
            {practice.explanation.includes("•") ? (
              <ul className="space-y-2 list-disc list-inside">
                {practice.explanation
                  .split("•")
                  .filter(Boolean)
                  .map((bullet, i) => (
                    <li key={i} className="leading-relaxed">
                      {bullet.trim()}
                    </li>
                  ))}
              </ul>
            ) : (
              <p className="leading-relaxed">{practice.explanation}</p>
            )}
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      <div
        className={cn(
          "transition-all duration-300 ease-in-out overflow-hidden",
          isExpanded ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0",
        )}
      >
        <div className="px-6 pb-6">
          <Separator className="mb-6" />

          {/* Quotes - Secondary Content */}
          {practice.quotes.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-zinc-600 mb-4 uppercase tracking-wide">Quotes</h4>
              <div className="space-y-4">
                {practice.quotes.map((quote) => (
                  <blockquote
                    key={quote.id}
                    className="group border-l-4 border-zinc-200 pl-4 py-2 bg-zinc-50/50 rounded-r-lg hover:border-zinc-300 hover:bg-zinc-50 transition-colors"
                  >
                    <p className="text-sm text-zinc-600 italic leading-relaxed mb-2">"{quote.text}"</p>
                    <footer className="flex items-center justify-between">
                      <div className="text-xs text-zinc-400">
                        {quote.speaker && <span className="font-medium">{quote.speaker}</span>}
                        {quote.speaker && quote.timestamp && <span className="mx-1">•</span>}
                        <span>{quote.timestamp}</span>
                      </div>
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          variant="ghost"
                          size="sm"
                          className="size-7 p-0 text-zinc-400 hover:text-zinc-600"
                          onClick={() => navigator.clipboard.writeText(quote.text)}
                        >
                          <Copy className="size-3" />
                        </Button>
                        <Button variant="ghost" size="sm" className="size-7 p-0 text-zinc-400 hover:text-zinc-600">
                          <Play className="size-3" />
                        </Button>
                      </div>
                    </footer>
                  </blockquote>
                ))}
              </div>
            </div>
          )}

          {/* Artifacts - Collapsible Code UI */}
          {practice.artifacts.length > 0 && (
            <div className="mb-6">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleArtifacts}
                className="text-sm font-semibold text-zinc-600 hover:text-zinc-900 p-0 h-auto gap-2 mb-3 uppercase tracking-wide"
              >
                <Code2 className="size-4" />
                {showArtifacts ? "Hide" : "Show"} Artifacts ({practice.artifacts.length})
              </Button>

              <div
                className={cn(
                  "transition-all duration-300 ease-in-out overflow-hidden",
                  showArtifacts ? "max-h-96 opacity-100" : "max-h-0 opacity-0",
                )}
              >
                <div className="bg-zinc-900 rounded-lg p-4 overflow-x-auto">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <div className="size-3 rounded-full bg-red-500"></div>
                        <div className="size-3 rounded-full bg-yellow-500"></div>
                        <div className="size-3 rounded-full bg-green-500"></div>
                      </div>
                      <span className="text-xs text-zinc-400 font-medium">ARTIFACTS</span>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="size-6 p-0 text-zinc-400 hover:text-zinc-200"
                      onClick={() => navigator.clipboard.writeText(practice.artifacts.join("\n"))}
                    >
                      <Copy className="size-3" />
                    </Button>
                  </div>
                  <div className="space-y-1">
                    {practice.artifacts.map((artifact, i) => (
                      <div key={i} className="text-sm font-mono text-zinc-300 leading-relaxed">
                        {artifact}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Tools Applied - Pills at Bottom */}
          {practiceTools.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-zinc-600 mb-3 uppercase tracking-wide">Tools Applied</h4>
              <div className="flex flex-wrap gap-2">
                {practiceTools.map((tool) => (
                  <Badge
                    key={tool.id}
                    variant="outline"
                    className="bg-gradient-to-r from-zinc-50 to-zinc-100 border-zinc-300 text-zinc-700 hover:from-zinc-100 hover:to-zinc-200 transition-all cursor-help px-3 py-1"
                    title={tool.purpose}
                  >
                    <span className="text-xs font-medium">{tool.name}</span>
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}
