import { Badge } from "@/components/ui/badge"

export function Principles({
  items = [],
}: {
  items: string[]
}) {
  if (!items.length) return null
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      {items.map((p) => (
        <Badge
          key={p}
          variant="secondary"
          className="rounded-full border border-zinc-200 bg-white px-3 py-1 text-zinc-700"
        >
          {p}
        </Badge>
      ))}
    </div>
  )
}
