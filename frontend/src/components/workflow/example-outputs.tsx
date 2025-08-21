/**
 * @fileoverview Optional outputs section rendering screenshots or external links.
 */

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { ExampleOutput } from "./types"
import { ExternalLink } from "lucide-react"

/**
 * @description Displays example outputs as images or link cards.
 */
export function ExampleOutputs({ items = [] }: { items?: ExampleOutput[] }) {
  if (!items || items.length === 0) return null

  return (
    <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
      {items.map((item, index) => {
        if (item.type === "image") {
          return (
            <Card key={index} className="overflow-hidden border-zinc-200/70 bg-white/70">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={item.src || "/placeholder.svg"} alt={item.alt} className="h-auto w-full" />
              <div className="p-4">
                <h4 className="text-sm font-medium text-zinc-900">{item.title || "Screenshot"}</h4>
              </div>
            </Card>
          )
        }
        if (item.type === "link") {
          return (
            <Card key={index} className="flex items-center justify-between gap-4 border-zinc-200/70 bg-white/70 p-4">
              <div className="min-w-0">
                <h4 className="truncate text-sm font-medium text-zinc-900">{item.title || item.label}</h4>
                <p className="mt-1 truncate text-sm text-zinc-600">{item.url}</p>
              </div>
              <Button asChild variant="outline" className="shrink-0 bg-transparent">
                <a href={item.url} target="_blank" rel="noreferrer">
                  <ExternalLink className="mr-2 size-4" aria-hidden="true" />
                  Open
                </a>
              </Button>
            </Card>
          )
        }
        throw new Error("Unsupported example output type")
      })}
    </div>
  )
}
