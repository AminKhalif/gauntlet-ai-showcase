import type { Metadata } from "next"
import { notFound } from "next/navigation"
import { WORKFLOWS } from "@/components/workflow/data"
import BuilderPageClient from "./BuilderPageClient"

export const metadata: Metadata = {
  title: "Flowdex - AI Builder Showcase",
}

export default function BuilderPage({
  params,
}: {
  params: { builderId: string }
}) {
  const builderId = params?.builderId
  const workflow = WORKFLOWS[builderId]
  if (!workflow) {
    notFound()
  }

  return <BuilderPageClient builderId={builderId} workflow={workflow} />
}
