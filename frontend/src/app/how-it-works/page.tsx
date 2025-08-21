/**
 * @fileoverview How it Works page explaining Flowdex pipeline and value proposition.
 */

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Upload, FileAudio, Brain, Layout, Users, CheckCircle, ArrowRight, Play } from "lucide-react"
import Link from "next/link"

/**
 * @description Explains how Flowdex works, who it's for, and provides clear CTAs.
 */
export default function HowItWorksPage() {
  return (
    <main className="min-h-screen bg-zinc-50">
      <div className="mx-auto max-w-4xl px-4 py-12 md:py-16">
        {/* Header */}
        <section className="text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900">How Flowdex Works</h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-zinc-600">
            Turn AI builder conversations into structured, comparable workflow profiles.
          </p>
        </section>

        <Separator className="my-12" />

        {/* What Flowdex Is */}
        <section aria-labelledby="what-is-heading" className="mb-12">
          <h2 id="what-is-heading" className="text-xl font-semibold text-zinc-900 mb-4">
            What Flowdex Is
          </h2>
          <p className="text-zinc-700 leading-relaxed">
            Flowdex showcases AI-first software workflows from real builders in a consistent format so you can compare
            approaches fast. Instead of scattered blog posts or long videos, get structured breakdowns of how different
            people actually build with AI tools.
          </p>
        </section>

        {/* How It Works Pipeline */}
        <section aria-labelledby="pipeline-heading" className="mb-12">
          <h2 id="pipeline-heading" className="text-xl font-semibold text-zinc-900 mb-6">
            How the Pipeline Works
          </h2>
          <div className="grid grid-cols-1 gap-4 md:gap-6">
            {[
              {
                icon: Upload,
                title: "Paste YouTube URL or Upload Audio",
                description:
                  "Start with a conversation, interview, or walkthrough where a builder explains their process.",
              },
              {
                icon: FileAudio,
                title: "Transcribe + Diarize",
                description: "Convert audio to text and identify who's speaking when for accurate attribution.",
              },
              {
                icon: Brain,
                title: "Extract Structured Data",
                description:
                  "AI identifies phases, practices, quotes, artifacts, and tools actually mentioned—no hallucinations.",
              },
              {
                icon: Layout,
                title: "Render Profile",
                description: "Generate a scannable profile with phase cards, practice sub-cards, and evidence drawers.",
              },
              {
                icon: Users,
                title: "Compare Across Builders",
                description: "Browse different approaches side-by-side to find patterns and differences.",
              },
            ].map((step, index) => {
              const Icon = step.icon
              return (
                <Card key={index} className="border-zinc-200/70 bg-white/70 p-4">
                  <div className="flex items-start gap-4">
                    <div className="flex size-10 items-center justify-center rounded-lg bg-zinc-100 text-zinc-700">
                      <Icon className="size-5" />
                    </div>
                    <div className="min-w-0">
                      <h3 className="font-medium text-zinc-900">{step.title}</h3>
                      <p className="mt-1 text-sm text-zinc-600">{step.description}</p>
                    </div>
                    {index < 4 && <ArrowRight className="size-4 text-zinc-400 mt-3 hidden md:block" />}
                  </div>
                </Card>
              )
            })}
          </div>
          <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-sm text-amber-800">
              <strong>Note:</strong> Quotes are verbatim from the source; we avoid hallucinations by grounding
              everything in the actual transcript.
            </p>
          </div>
        </section>

        {/* What You Get */}
        <section aria-labelledby="benefits-heading" className="mb-12">
          <h2 id="benefits-heading" className="text-xl font-semibold text-zinc-900 mb-4">
            What You Get
          </h2>
          <ul className="grid grid-cols-1 gap-3 md:grid-cols-2">
            {[
              "Glanceable layout (phases → practices)",
              "Verbatim quotes for proof",
              "Tools-per-phase, not hand-wavy lists",
              '"Show evidence" drawers for deep dives',
            ].map((benefit) => (
              <li key={benefit} className="flex items-center gap-3">
                <CheckCircle className="size-5 text-emerald-600" />
                <span className="text-zinc-700">{benefit}</span>
              </li>
            ))}
          </ul>
        </section>

        {/* Who It's For */}
        <section aria-labelledby="audience-heading" className="mb-12">
          <h2 id="audience-heading" className="text-xl font-semibold text-zinc-900 mb-4">
            Who It's For
          </h2>
          <div className="flex flex-wrap gap-2">
            {["Hiring partners (Gauntlet)", "Founders", "AI-first engineers", "Students"].map((audience) => (
              <Badge key={audience} variant="secondary" className="px-3 py-1">
                {audience}
              </Badge>
            ))}
          </div>
        </section>

        {/* Try It */}
        <section aria-labelledby="cta-heading" className="mb-12">
          <h2 id="cta-heading" className="text-xl font-semibold text-zinc-900 mb-4">
            Try It
          </h2>
          <div className="flex flex-col gap-4 sm:flex-row">
            <Button size="lg" className="bg-zinc-900 hover:bg-zinc-800">
              Create Profile
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/">
                <Play className="mr-2 size-4" />
                Browse Builders
              </Link>
            </Button>
          </div>
        </section>

        {/* FAQ */}
        <section aria-labelledby="faq-heading">
          <h2 id="faq-heading" className="text-xl font-semibold text-zinc-900 mb-6">
            FAQ
          </h2>
          <div className="space-y-6">
            {[
              {
                question: "How do you handle tools mentioned vs. used?",
                answer:
                  "We distinguish between tools casually mentioned and tools actually demonstrated or described in detail. Only the latter appear in the 'Tools used in this phase' sections.",
              },
              {
                question: "How do you avoid hallucinations?",
                answer:
                  "All quotes are verbatim from transcripts. Practices and artifacts are extracted conservatively—if it's not clearly stated or shown, it doesn't make it into the profile.",
              },
              {
                question: "Can I edit a profile after extraction?",
                answer:
                  "Yes, profiles can be reviewed and refined. The initial extraction provides a strong foundation that can be polished for accuracy and clarity.",
              },
            ].map((faq) => (
              <Card key={faq.question} className="border-zinc-200/70 bg-white/70 p-4">
                <h3 className="font-medium text-zinc-900 mb-2">{faq.question}</h3>
                <p className="text-sm text-zinc-600">{faq.answer}</p>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
