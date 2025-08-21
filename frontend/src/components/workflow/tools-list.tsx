/**
 * @fileoverview Tool list grid showing name, category, and workflow purpose.
 */

import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import type { Tool } from "./types"
import { iconMap, getCategoryColor, cn } from "./utils"

/**
 * @description Displays tools as a responsive grid with category badges and purposes.
 */
export function ToolsList({ tools = [] }: { tools: Tool[] }) {
  return (
    <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {tools.map((tool) => {
        const Icon = tool.icon ? iconMap[tool.icon] : iconMap.Code2
        const color = getCategoryColor(tool.category)
        return (
          <Card
            key={tool.id}
            className="group border-zinc-200/70 bg-white/60 p-4 transition-colors hover:border-zinc-300"
          >
            <div className="flex items-start gap-3">
              <div
                className={cn("flex size-10 items-center justify-center rounded-md ring-1", color)}
                aria-hidden="true"
              >
                <Icon className="size-5" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="truncate font-medium text-zinc-900">{tool.name}</h3>
                  <Badge variant="secondary" className={cn("rounded-full px-2 py-0.5 text-xs ring-1", color)}>
                    {tool.category}
                  </Badge>
                </div>
                <p className="mt-1 text-sm text-zinc-600">{tool.purpose}</p>
              </div>
            </div>
          </Card>
        )
      })}
    </div>
  )
}
