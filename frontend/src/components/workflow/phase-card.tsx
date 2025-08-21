/**
 * @fileoverview Polished phase card with compact practices, explanation-first design, and collapsible quotes.
 */

"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ChevronDown, ChevronUp, Copy, Play, Eye, EyeOff } from "lucide-react"
import type { PhaseData, PracticeData, QuoteData } from "./types"

type PhaseCardProps = {
  phase: PhaseData
  isExpanded?: boolean
  onToggleExpanded?: () => void
}

/**
 * @description Renders a phase with summary, tools, and collapsible practice cards with explanation-first design.
 */
export function PhaseCard({ phase, isExpanded = false, onToggleExpanded }: PhaseCardProps) {
  const [expandedPractices, setExpandedPractices] = useState<Set<string>>(new Set())
  const [showAllPractices, setShowAllPractices] = useState(false)

  const togglePractice = (practiceId: string) => {
    const newExpanded = new Set(expandedPractices)
    if (newExpanded.has(practiceId)) {
      newExpanded.delete(practiceId)
    } else {
      newExpanded.add(practiceId)
    }
    setExpandedPractices(newExpanded)
  }

  const toggleAllPractices = () => {
    if (expandedPractices.size === phase.practices.length) {
      setExpandedPractices(new Set())
    } else {
      setExpandedPractices(new Set(phase.practices.map((p) => p.id)))
    }
  }

  const visiblePractices = showAllPractices ? phase.practices : phase.practices.slice(0, 3)
  const hasMorePractices = phase.practices.length > 3

  return (
    <Card className="border-zinc-200/70 bg-white/70 p-4 md:p-5">
      {/* Phase Header */}
      <header className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
        <div className="min-w-0 flex-1">
          <h2 className="text-lg font-semibold text-zinc-900">{phase.title}</h2>
          <p className="mt-1 text-sm text-zinc-600 leading-relaxed">{phase.summary}</p>
        </div>

        {/* Tools Used */}
        {phase.toolsUsed?.length ? (
          <div className="flex flex-wrap gap-1.5 md:max-w-xs">
            <span className="text-xs text-zinc-500 w-full md:w-auto">Tools used:</span>
            {phase.toolsUsed.map((tool) => (
              <Badge key={tool} variant="outline" className="text-xs px-2 py-0.5">
                {tool}
              </Badge>
            ))}
          </div>
        ) : null}
      </header>

      {/* Expand/Collapse All */}
      {phase.practices.length > 1 && (
        <div className="mt-4 flex items-center justify-between">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleAllPractices}
            className="text-xs text-zinc-600 hover:text-zinc-900"
          >
            {expandedPractices.size === phase.practices.length ? "Collapse all" : "Expand all"}
          </Button>
        </div>
      )}

      <Separator className="my-4" />

      {/* Practices */}
      <div className="space-y-3">
        {visiblePractices.map((practice) => (
          <PracticeCard
            key={practice.id}
            practice={practice}
            isExpanded={expandedPractices.has(practice.id)}
            onToggle={() => togglePractice(practice.id)}
          />
        ))}

        {hasMorePractices && !showAllPractices && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowAllPractices(true)}
            className="w-full text-xs text-zinc-600 hover:text-zinc-900"
          >
            Show more practices ({phase.practices.length - 3})
          </Button>
        )}
      </div>
    </Card>
  )
}

type PracticeCardProps = {
  practice: PracticeData
  isExpanded: boolean
  onToggle: () => void
}

/**
 * @description Individual practice card with explanation-first design and compact quotes.
 */
function PracticeCard({ practice, isExpanded, onToggle }: PracticeCardProps) {
  const [showAllQuotes, setShowAllQuotes] = useState(false)
  const [showArtifacts, setShowArtifacts] = useState(false)
  const [expandedQuotes, setExpandedQuotes] = useState<Set<string>>(new Set())

  const toggleQuote = (quoteId: string) => {
    const newExpanded = new Set(expandedQuotes)
    if (newExpanded.has(quoteId)) {
      newExpanded.delete(quoteId)
    } else {
      newExpanded.add(quoteId)
    }
    setExpandedQuotes(newExpanded)
  }

  const visibleQuotes = showAllQuotes ? practice.quotes : practice.quotes.slice(0, 2)
  const hasMoreQuotes = practice.quotes.length > 2

  return (
    <Card className="border-zinc-200/50 bg-zinc-50/50 p-3">
      {/* Title Row */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <Badge variant="secondary" className="text-xs px-2 py-0.5 shrink-0">
            {practice.type}
          </Badge>
          <h3 className="font-medium text-zinc-900 truncate">{practice.title}</h3>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggle}
          className="shrink-0 text-xs text-zinc-600 hover:text-zinc-900"
        >
          {isExpanded ? (
            <>
              <ChevronUp className="size-3 mr-1" />
              Collapse
            </>
          ) : (
            <>
              <ChevronDown className="size-3 mr-1" />
              Expand
            </>
          )}
        </Button>
      </div>

      {/* Collapsed View */}
      {!isExpanded && <p className="mt-2 text-sm text-zinc-600 line-clamp-2">{practice.explanation}</p>}

      {/* Expanded View */}
      {isExpanded && (
        <div className="mt-3 space-y-4">
          {/* Explanation - Primary Content */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Explanation</span>
            </div>
            <div className="text-sm text-zinc-700 leading-relaxed font-medium">
              {practice.explanation.includes("•") ? (
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
              )}
            </div>
          </div>

          {/* Quotes - Secondary Content */}
          {practice.quotes.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Quotes</span>
              </div>
              <div className="space-y-2">
                {visibleQuotes.map((quote) => (
                  <QuoteRow
                    key={quote.id}
                    quote={quote}
                    isExpanded={expandedQuotes.has(quote.id)}
                    onToggle={() => toggleQuote(quote.id)}
                  />
                ))}
                {hasMoreQuotes && !showAllQuotes && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowAllQuotes(true)}
                    className="text-xs text-zinc-500 hover:text-zinc-700"
                  >
                    Show more quotes ({practice.quotes.length - 2})
                  </Button>
                )}
              </div>
            </div>
          )}

          {practice.quotes.length === 0 && <div className="text-xs text-zinc-400 italic">No quotes captured.</div>}

          {/* Artifacts - Collapsed by Default */}
          {practice.artifacts.length > 0 && (
            <div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowArtifacts(!showArtifacts)}
                className="text-xs text-zinc-600 hover:text-zinc-900 p-0"
              >
                {showArtifacts ? <EyeOff className="size-3 mr-1" /> : <Eye className="size-3 mr-1" />}
                {showArtifacts ? "Hide" : "Show"} artifacts ({practice.artifacts.length})
              </Button>
              {showArtifacts && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {practice.artifacts.map((artifact, i) => (
                    <Badge key={i} variant="outline" className="text-xs">
                      {artifact}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
          )}

          {practice.artifacts.length === 0 && <div className="text-xs text-zinc-400 italic">No artifacts.</div>}
        </div>
      )}
    </Card>
  )
}

type QuoteRowProps = {
  quote: QuoteData
  isExpanded: boolean
  onToggle: () => void
}

/**
 * @description Compact quote row with expand/collapse and action buttons.
 */
function QuoteRow({ quote, isExpanded, onToggle }: QuoteRowProps) {
  const truncatedText = quote.text.length > 80 ? quote.text.slice(0, 80) + "…" : quote.text

  const handleCopy = () => {
    navigator.clipboard.writeText(quote.text)
  }

  const handlePlay = () => {
    // Placeholder for play functionality
    console.log("Play quote at", quote.timestamp)
  }

  return (
    <div className="text-xs text-zinc-600">
      {!isExpanded ? (
        <button
          onClick={onToggle}
          className="flex items-center gap-2 text-left hover:text-zinc-800 transition-colors w-full"
        >
          <span>❝ {truncatedText} ❞</span>
          <span className="text-zinc-400">•</span>
          <span className="text-zinc-400">{quote.timestamp}</span>
          <div className="flex items-center gap-1 ml-auto">
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                handleCopy()
              }}
              className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
            >
              <Copy className="size-3" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                handlePlay()
              }}
              className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
            >
              <Play className="size-3" />
            </Button>
          </div>
        </button>
      ) : (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-zinc-400">{quote.timestamp}</span>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleCopy}
                className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
              >
                <Copy className="size-3" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handlePlay}
                className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
              >
                <Play className="size-3" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={onToggle}
                className="size-6 p-0 text-zinc-400 hover:text-zinc-600"
              >
                <ChevronUp className="size-3" />
              </Button>
            </div>
          </div>
          <blockquote className="border-l-2 border-zinc-200 pl-3 py-2 bg-zinc-50 rounded-r text-zinc-700 text-sm leading-relaxed">
            {quote.text}
          </blockquote>
        </div>
      )}
    </div>
  )
}
