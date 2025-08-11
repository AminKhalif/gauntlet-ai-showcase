import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ExternalLink } from "lucide-react"
import type { Builder } from "./types"

export function BuilderHeader({
  builder,
}: {
  builder: Builder
}) {
  const initials = builder.name
    .split(" ")
    .map((s) => s[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <header className="relative">
      <Card className="border-zinc-200/70 bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="flex flex-col items-start gap-4 p-5 md:flex-row md:items-center md:p-6">
          <div className="flex items-center gap-4">
            <Avatar className="size-16 ring-2 ring-zinc-200">
              <AvatarImage src={builder.avatar || "/placeholder.svg"} alt={`${builder.name} avatar`} />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div>
              <h1 className="text-xl md:text-2xl font-semibold tracking-tight text-zinc-900">{builder.name}</h1>
              <p className="text-sm text-zinc-600">{builder.role}</p>
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
      </Card>
    </header>
  )
}
