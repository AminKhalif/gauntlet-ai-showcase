import {
  Bot,
  SquareTerminal,
  Sparkles,
  FlaskConical,
  Network,
  Workflow,
  Code2,
  Wrench,
  Lightbulb,
  Quote,
  ImageIcon,
} from "lucide-react"

export const iconMap = {
  Bot,
  SquareTerminal,
  Sparkles,
  FlaskConical,
  Network,
  Workflow,
  Code2,
  Wrench,
  Lightbulb,
  Quote,
  Image: ImageIcon,
}

export type IconName = keyof typeof iconMap

export function getCategoryColor(category: string): string {
  const key = category.toLowerCase()
  if (key.includes("code")) return "bg-emerald-50 text-emerald-700 ring-emerald-200"
  if (key.includes("test")) return "bg-amber-50 text-amber-700 ring-amber-200"
  if (key.includes("debug") || key.includes("api")) return "bg-rose-50 text-rose-700 ring-rose-200"
  if (key.includes("chain")) return "bg-violet-50 text-violet-700 ring-violet-200"
  if (key.includes("ide") || key.includes("editor")) return "bg-cyan-50 text-cyan-700 ring-cyan-200"
  return "bg-zinc-50 text-zinc-700 ring-zinc-200"
}

export function cn(...classes: (string | false | null | undefined)[]) {
  return classes.filter(Boolean).join(" ")
}
