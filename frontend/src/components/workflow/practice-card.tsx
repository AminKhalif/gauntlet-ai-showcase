/**
 * @fileoverview Compact practice card with prominent explanations and secondary quotes.
 */

"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp, Code2, Copy, Play } from "lucide-react"
import type { PracticeData, Workflow } from "./types"
import { cn } from "./utils"

type PracticeCardProps = {
  practice: PracticeData
  workflow: Workflow
}

/**
 * @description Compact practice card with explanation-first design and collapsible content.
 */
export function PracticeCard({ practice, workflow }: PracticeCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [showAllQuotes, setShowAllQuotes] = useState(false)
  const [showArtifacts, setShowArtifacts] = useState(false)

  const toggleExpanded = () => setIsExpanded(!isExpanded)
  const toggleAllQuotes = () => setShowAllQuotes(!showAllQuotes)
  const toggleArtifacts = () => setShowArtifacts(!showArtifacts)

  const typeColors = {
    Rule: "bg-red-50 text-red-700 border-red-200",
    Practice: "bg-blue-50 text-blue-700 border-blue-200",
    Method: "bg-emerald-50 text-emerald-700 border-emerald-200",
  }

  const typeColor = typeColors[practice.type as keyof typeof typeColors] || typeColors.Practice

  // Get tools mentioned in this practice
  const practiceTools = workflow.tools.filter(
    (tool) =>
      practice.explanation.toLowerCase().includes(tool.name.toLowerCase()) ||
      practice.quotes.some((quote) => quote.text.toLowerCase().includes(tool.name.toLowerCase())),
  )

  const visibleQuotes = showAllQuotes ? practice.quotes : practice.quotes.slice(0, 2)
  const hasMoreQuotes = practice.quotes.length > 2

  // Truncate explanation for collapsed view
  const shouldTruncateExplanation = practice.explanation.length > 200
  const truncatedExplanation = shouldTruncateExplanation
    ? practice.explanation.slice(0, 200) + "..."
    : practice.explanation

  return (
    <Card className="border-zinc-200 bg-zinc-50/50 hover:bg-zinc-50 transition-colors">
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <Badge className={cn("text-xs px-2 py-1 border", typeColor)}>{practice.type}</Badge>
            <h3 className="font-semibold text-zinc-900 truncate">{practice.title}</h3>
          </div>
          {(shouldTruncateExplanation || practice.quotes.length > 0 || practice.artifacts.length > 0) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleExpanded}
              className="shrink-0 text-zinc-500 hover:text-zinc-700"
            >
              {isExpanded ? <ChevronUp className="size-4" /> : <ChevronDown className="size-4" />}
            </Button>
          )}
        </div>

        {/* Explanation - Primary Content */}
        <div className="mb-3">
          <div className="text-base text-zinc-800 leading-relaxed font-medium">
            {isExpanded || !shouldTruncateExplanation ? (
              practice.explanation.includes("•") ? (
                <ul className="space-y-1 list-disc list-inside">
                  {practice.explanation
                    .split("•")
                    .filter(Boolean)
                    .map((bullet, i) => (
                      <li key={i}>{bullet.trim()}</li>
                    ))}
                </ul>
              ) : (
                <p>{practice.explanation}</p>
              )
            ) : (
              <p>{truncatedExplanation}</p>
            )}
          </div>
        </div>

        {/* Expanded Content */}
        {isExpanded && (
          <div className="space-y-4 border-t border-zinc-200 pt-4">
            {/* Quotes - Secondary Content */}
            {practice.quotes.length > 0 && (
              <div>
                <div className="space-y-2">
                  {visibleQuotes.map((quote) => (
                    <blockquote
                      key={quote.id}
                      className="border-l-3 border-zinc-300 pl-3 py-1 bg-white/50 rounded-r text-sm"
                    >
                      <p className="text-zinc-600 italic leading-relaxed">"{quote.text}"</p>
                      <footer className="mt-1 flex items-center justify-between">
                        <div className="text-xs text-zinc-400">
                          {quote.speaker && <span className="font-medium">{quote.speaker}</span>}
                          {quote.speaker && quote.timestamp && <span className="mx-1">•</span>}
                          <span>{quote.timestamp}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
                            onClick={() => navigator.clipboard.writeText(quote.text)}
                          >
                            <Copy className="size-3" />
                          </Button>
                          <Button variant="ghost" size="sm" className="size-6 p-0 text-zinc-400 hover:text-zinc-600">
                            <Play className="size-3" />
                          </Button>
                        </div>
                      </footer>
                    </blockquote>
                  ))}
                </div>

                {hasMoreQuotes && !showAllQuotes && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={toggleAllQuotes}
                    className="text-xs text-zinc-600 hover:text-zinc-900 p-0 h-auto"
                  >
                    Show more quotes ({practice.quotes.length - 2})
                  </Button>
                )}
              </div>
            )}

            {/* Artifacts - Tertiary Content */}
            {practice.artifacts.length > 0 && (
              <div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={toggleArtifacts}
                  className="text-xs font-medium text-zinc-600 hover:text-zinc-900 p-0 h-auto gap-2 mb-2"
                >
                  <Code2 className="size-3" />
                  {showArtifacts ? "Hide" : "Show"} artifacts ({practice.artifacts.length})
                </Button>

                {showArtifacts && (
                  <div className="bg-zinc-900 rounded-lg p-3 overflow-x-auto">
                    <div className="space-y-1">
                      {practice.artifacts.map((artifact, i) => (
                        <div key={i} className="text-sm font-mono text-zinc-300">
                          {artifact}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Tools Applied */}
            {practiceTools.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {practiceTools.map((tool) => (
                  <Badge
                    key={tool.id}
                    variant="outline"
                    className="text-xs bg-white border-zinc-300 text-zinc-600 hover:bg-zinc-50"
                    title={tool.purpose}
                  >
                    {tool.name}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </Card>
  )
}
