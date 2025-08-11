import Link from "next/link"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { WORKFLOWS } from "@/components/workflow/data"

export default function IndexPage() {
  const items = Object.values(WORKFLOWS)

  return (
    <main className="min-h-screen bg-zinc-50">
      <div className="mx-auto max-w-6xl px-4 py-10 md:py-14">
        <section className="text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900">AI Workflow Showcase</h1>
          <p className="mx-auto mt-3 max-w-2xl text-zinc-600">
            Premium developer workflows powered by AI. Explore builder profiles, tools, principles, and detailed
            step-by-step guides.
          </p>
        </section>

        <Separator className="my-10" />

        <section aria-labelledby="workflows-heading">
          <h2 id="workflows-heading" className="sr-only">
            Workflows
          </h2>
          <ul className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((wf) => {
              const initials = wf.builder.name
                .split(" ")
                .map((s) => s[0])
                .join("")
                .slice(0, 2)
                .toUpperCase()
              return (
                <li key={wf.slug}>
                  <Link href={`/workflows/${wf.slug}`} className="block focus:outline-none">
                    <Card className="h-full border-zinc-200/70 bg-white/70 p-5 transition-colors hover:border-zinc-300 focus-visible:ring-2">
                      <div className="flex items-center gap-3">
                        <Avatar className="size-12 ring-1 ring-zinc-200">
                          <AvatarImage
                            src={wf.builder.avatar || "/placeholder.svg"}
                            alt={`${wf.builder.name} avatar`}
                          />
                          <AvatarFallback>{initials}</AvatarFallback>
                        </Avatar>
                        <div className="min-w-0">
                          <h3 className="truncate text-base font-semibold text-zinc-900">{wf.builder.name}</h3>
                          <p className="truncate text-sm text-zinc-600">{wf.builder.role}</p>
                        </div>
                      </div>
                      <p className="mt-3 line-clamp-3 text-sm leading-relaxed text-zinc-600">{wf.summary}</p>
                      {wf.tools?.length ? (
                        <div className="mt-4 flex flex-wrap gap-1.5">
                          {wf.tools.slice(0, 3).map((t) => (
                            <Badge key={t.id} variant="secondary" className="rounded-full">
                              {t.name}
                            </Badge>
                          ))}
                          {wf.tools.length > 3 ? (
                            <span className="text-xs text-zinc-500">+{wf.tools.length - 3} more</span>
                          ) : null}
                        </div>
                      ) : null}
                    </Card>
                  </Link>
                </li>
              )
            })}
          </ul>
        </section>
      </div>
    </main>
  )
}
