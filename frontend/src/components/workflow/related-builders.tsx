/**
 * @fileoverview Horizontal scroller of related builder cards with shared patterns.
 */

import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import type { RelatedBuilder } from "./types"

/**
 * @description Renders related builders in a horizontally scrollable list.
 */
export function RelatedBuilders({ builders = [] }: { builders?: RelatedBuilder[] }) {
  if (!builders || builders.length === 0) return null

  return (
    <div className="mt-4 overflow-x-auto">
      <ul className="flex w-full min-w-0 gap-4 pb-2">
        {builders.map((builder) => {
          const initials = builder.name
            .split(" ")
            .map((s) => s[0])
            .join("")
            .slice(0, 2)
            .toUpperCase()
          return (
            <li key={builder.name} className="min-w-[260px] max-w-[280px]">
              <Card className="h-full border-zinc-200/70 bg-white/70 p-4">
                <div className="flex items-center gap-3">
                  <Avatar className="size-10 ring-1 ring-zinc-200">
                    <AvatarImage
                      src={builder.avatar || "/placeholder.svg?height=96&width=96&query=builder-avatar"}
                      alt={`${builder.name} avatar`}
                    />
                    <AvatarFallback>{initials}</AvatarFallback>
                  </Avatar>
                  <div className="min-w-0">
                    <h4 className="truncate text-sm font-semibold text-zinc-900">{builder.name}</h4>
                    <p className="truncate text-xs text-zinc-600">{builder.role}</p>
                  </div>
                </div>
                {builder.shared && builder.shared.length > 0 ? (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {builder.shared.map((sharedItem) => (
                      <span
                        key={sharedItem}
                        className="rounded-full border border-zinc-200 bg-zinc-50 px-2 py-0.5 text-[10px] text-zinc-700"
                      >
                        {sharedItem}
                      </span>
                    ))}
                  </div>
                ) : null}
              </Card>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
