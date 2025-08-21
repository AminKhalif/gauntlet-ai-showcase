import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { TopNav } from "@/components/layout/top-nav"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Flowdex - AI Builder Showcase",
  description: "Real workflows from builders using AI tools. See how they actually work, phase by phase.",
}

/**
 * @description Root layout providing navigation and base styling for all pages.
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <TopNav />
        {children}
      </body>
    </html>
  )
}
