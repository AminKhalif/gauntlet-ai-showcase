import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import type { RelatedBuilder } from "./types"

export function RelatedBuilders({
  builders = [],
}: {
  builders?: RelatedBuilder[]
}) {
  if (!builders || builders.length === 0) return null

  return (
    <div className="mt-4 overflow-x-auto">
      <ul className="flex w-full min-w-0 gap-4 pb-2">
        {builders.map((b) => {
          const initials = b.name
            .split(" ")
            .map((s) => s[0])
            .join("")
            .slice(0, 2)
            .toUpperCase()
          return (
            <li key={b.name} className="min-w-[260px] max-w-[280px]">
              <Card className="h-full border-zinc-200/70 bg-white/70 p-4">
                <div className="flex items-center gap-3">
                  <Avatar className="size-10 ring-1 ring-zinc-200">
                    <AvatarImage src={b.avatar || "/placeholder.svg"} alt={`${b.name} avatar`} />
                    <AvatarFallback>{initials}</AvatarFallback>
                  </Avatar>
                  <div className="min-w-0">
                    <h4 className="truncate text-sm font-semibold text-zinc-900">{b.name}</h4>
                    <p className="truncate text-xs text-zinc-600">{b.role}</p>
                  </div>
                </div>
                {b.shared && b.shared.length > 0 ? (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {b.shared.map((s) => (
                      <span
                        key={s}
                        className="rounded-full border border-zinc-200 bg-zinc-50 px-2 py-0.5 text-[10px] text-zinc-700"
                      >
                        {s}
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
