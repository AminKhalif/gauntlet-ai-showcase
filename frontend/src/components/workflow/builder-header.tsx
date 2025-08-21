/**
 * @fileoverview Clean builder header with modern SaaS styling.
 */

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ExternalLink } from "lucide-react"
import type { Builder } from "./types"

/**
 * @description Clean builder header with modern styling and clear hierarchy.
 */
export function BuilderHeader({ builder }: { builder: Builder }) {
  const initials = builder.name
    .split(" ")
    .map((segment) => segment[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <header className="relative">
      <Card className="border-zinc-200 bg-white shadow-sm">
        <div className="p-8">
          <div className="flex flex-col items-start gap-6 md:flex-row md:items-center">
            <div className="flex items-center gap-6">
              <Avatar className="size-20 ring-2 ring-zinc-200">
                <AvatarImage
                  src={builder.avatar || "/placeholder.svg?height=128&width=128&query=builder-avatar"}
                  alt={`${builder.name} avatar`}
                />
                <AvatarFallback className="text-lg font-semibold">{initials}</AvatarFallback>
              </Avatar>
              <div>
                <h1 className="text-3xl font-bold tracking-tight text-zinc-900">{builder.name}</h1>
                <p className="text-lg text-zinc-600 mt-1">{builder.role}</p>
              </div>
            </div>
            <div className="flex-1" />
            {builder.sourceUrl ? (
              <Button asChild variant="outline" className="gap-2 bg-transparent">
                <a href={builder.sourceUrl} target="_blank" rel="noreferrer">
                  <ExternalLink className="size-4" aria-hidden="true" />
                  <span className="sr-only">Open original source</span>
                  View Original
                </a>
              </Button>
            ) : null}
          </div>
        </div>
      </Card>
    </header>
  )
}
