/**
 * @fileoverview Small tag list for principles and patterns used by a builder.
 */

import { Badge } from "@/components/ui/badge"

/**
 * @description Renders a list of principle tags or returns null when empty.
 */
export function Principles({ items = [] }: { items: string[] }) {
  if (!items.length) return null
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      {items.map((principle) => (
        <Badge
          key={principle}
          variant="secondary"
          className="rounded-full border border-zinc-200 bg-white px-3 py-1 text-zinc-700"
        >
          {principle}
        </Badge>
      ))}
    </div>
  )
}
