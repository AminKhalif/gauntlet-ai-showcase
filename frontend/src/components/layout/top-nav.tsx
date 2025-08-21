/**
 * @fileoverview Clean top navigation with Add Builder modal integration.
 */

"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { AddBuilderModal } from "@/components/modals/add-builder-modal"
import { Menu, X } from "lucide-react"

/**
 * @description Clean top navigation with modal integration and responsive mobile menu.
 */
export function TopNav() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isAddBuilderModalOpen, setIsAddBuilderModalOpen] = useState(false)

  const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen)
  const closeMobileMenu = () => setIsMobileMenuOpen(false)
  const openAddBuilderModal = () => setIsAddBuilderModalOpen(true)
  const closeAddBuilderModal = () => setIsAddBuilderModalOpen(false)

  return (
    <>
      <nav className="sticky top-0 z-50 border-b border-zinc-200 bg-white">
        <div className="mx-auto max-w-7xl px-4">
          <div className="flex h-16 items-center justify-between">
            {/* Brand */}
            <Link
              href="/"
              className="text-xl font-semibold tracking-tight text-zinc-900 hover:text-zinc-700 transition-colors"
              onClick={closeMobileMenu}
            >
              Flowdex
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex md:items-center md:gap-8">
              <Link href="/" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors">
                Builders
              </Link>
              <Link
                href="/how-it-works"
                className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors"
              >
                How it Works
              </Link>
              <Button onClick={openAddBuilderModal} className="bg-zinc-900 hover:bg-zinc-800">
                Add Builder
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={toggleMobileMenu}
              aria-label={isMobileMenuOpen ? "Close menu" : "Open menu"}
            >
              {isMobileMenuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
            </Button>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
            <div className="border-t border-zinc-200 bg-white py-4 md:hidden">
              <div className="flex flex-col gap-4">
                <Link
                  href="/"
                  className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors"
                  onClick={closeMobileMenu}
                >
                  Builders
                </Link>
                <Link
                  href="/how-it-works"
                  className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors"
                  onClick={closeMobileMenu}
                >
                  How it Works
                </Link>
                <Button
                  onClick={() => {
                    openAddBuilderModal()
                    closeMobileMenu()
                  }}
                  className="w-fit bg-zinc-900 hover:bg-zinc-800"
                >
                  Add Builder
                </Button>
              </div>
            </div>
          )}
        </div>
      </nav>

      <AddBuilderModal isOpen={isAddBuilderModalOpen} onClose={closeAddBuilderModal} />
    </>
  )
}
