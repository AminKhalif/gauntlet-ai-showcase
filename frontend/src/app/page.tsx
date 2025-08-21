/**
 * @fileoverview Clean library page with Add Builder modal integration.
 */

"use client"

import { useState } from "react"
import Link from "next/link"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { AddBuilderModal } from "@/components/modals/add-builder-modal"
import { WORKFLOWS } from "@/components/workflow/data"

/**
 * @description Clean library page showcasing builder workflows with modal integration.
 */
export default function LibraryPage() {
  const [isAddBuilderModalOpen, setIsAddBuilderModalOpen] = useState(false)
  const workflows = Object.values(WORKFLOWS)

  if (workflows.length === 0) {
    throw new Error("No workflows available. Add at least one workflow to render the library.")
  }

  return (
    <>
      <main className="min-h-screen bg-zinc-50">
        <div className="mx-auto max-w-6xl px-4 py-12 md:py-16">
          {/* Hero Section */}
          <section className="text-center">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900">AI Builder Showcase</h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-zinc-600">
              Real workflows from builders using AI tools. See how they actually work, phase by phase.
            </p>
            <div className="mt-8">
              <Button
                size="lg"
                className="bg-zinc-900 hover:bg-zinc-800"
                onClick={() => setIsAddBuilderModalOpen(true)}
              >
                Add Builder
              </Button>
            </div>
          </section>

          {/* Builders Grid */}
          <section aria-labelledby="builders-heading" className="mt-16">
            <h2 id="builders-heading" className="sr-only">
              Available Builders
            </h2>
            <ul className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {workflows.map((workflow) => {
                const initials = workflow.builder.name
                  .split(" ")
                  .map((s) => s[0])
                  .join("")
                  .slice(0, 2)
                  .toUpperCase()

                return (
                  <li key={workflow.slug}>
                    <Link href={`/builders/${workflow.slug}`} className="block focus:outline-none">
                      <Card className="h-full border-zinc-200 bg-white p-6 transition-all hover:border-zinc-300 hover:shadow-sm focus-visible:ring-2">
                        <div className="flex items-center gap-4">
                          <Avatar className="size-14 ring-2 ring-zinc-200">
                            <AvatarImage
                              src={
                                workflow.builder.avatar || "/placeholder.svg?height=96&width=96&query=builder-avatar"
                              }
                              alt={`${workflow.builder.name} avatar`}
                            />
                            <AvatarFallback className="text-sm font-medium">{initials}</AvatarFallback>
                          </Avatar>
                          <div className="min-w-0">
                            <h3 className="truncate text-lg font-semibold text-zinc-900">{workflow.builder.name}</h3>
                            <p className="truncate text-sm text-zinc-600">{workflow.builder.role}</p>
                          </div>
                        </div>
                        <p className="mt-4 line-clamp-3 text-sm leading-relaxed text-zinc-700">{workflow.summary}</p>
                        {workflow.tools?.length ? (
                          <div className="mt-4 flex flex-wrap gap-2">
                            {workflow.tools.slice(0, 4).map((tool) => (
                              <Badge key={tool.id} variant="secondary" className="rounded-full text-xs">
                                {tool.name}
                              </Badge>
                            ))}
                            {workflow.tools.length > 4 ? (
                              <span className="text-xs text-zinc-500">+{workflow.tools.length - 4} more</span>
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

      <AddBuilderModal isOpen={isAddBuilderModalOpen} onClose={() => setIsAddBuilderModalOpen(false)} />
    </>
  )
}
