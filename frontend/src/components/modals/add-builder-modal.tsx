/**
 * @fileoverview Premium Add Builder modal with form validation and clean design.
 */

"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ExternalLink } from "lucide-react"
import Link from "next/link"

type AddBuilderModalProps = {
  isOpen: boolean
  onClose: () => void
}

type FormData = {
  firstName: string
  lastName: string
  youtubeUrl: string
}

type FormErrors = {
  firstName?: string
  lastName?: string
  youtubeUrl?: string
}

/**
 * @description Modal for adding a new builder with form validation and premium styling.
 */
export function AddBuilderModal({ isOpen, onClose }: AddBuilderModalProps) {
  const [formData, setFormData] = useState<FormData>({
    firstName: "",
    lastName: "",
    youtubeUrl: "",
  })
  const [errors, setErrors] = useState<FormErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateYouTubeUrl = (url: string): boolean => {
    if (!url) return false
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/
    return youtubeRegex.test(url)
  }

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.firstName.trim()) {
      newErrors.firstName = "First name is required"
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = "Last name is required"
    }

    if (!formData.youtubeUrl.trim()) {
      newErrors.youtubeUrl = "YouTube URL is required"
    } else if (!validateYouTubeUrl(formData.youtubeUrl)) {
      newErrors.youtubeUrl = "Please enter a valid YouTube URL"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) return

    setIsSubmitting(true)

    // Mock submission - replace with actual API call
    await new Promise((resolve) => setTimeout(resolve, 1500))

    setIsSubmitting(false)
    onClose()

    // Reset form
    setFormData({ firstName: "", lastName: "", youtubeUrl: "" })
    setErrors({})
  }

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }))
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader className="space-y-3">
          <DialogTitle className="text-xl font-semibold text-zinc-900">Add Builder</DialogTitle>
          <p className="text-sm text-zinc-600">Create a new builder profile from a YouTube video or interview.</p>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            {/* First Name */}
            <div className="space-y-2">
              <Label htmlFor="firstName" className="text-sm font-medium text-zinc-700">
                First name
              </Label>
              <Input
                id="firstName"
                type="text"
                placeholder="e.g. Jane"
                value={formData.firstName}
                onChange={(e) => handleInputChange("firstName", e.target.value)}
                className={errors.firstName ? "border-red-300 focus:border-red-500 focus:ring-red-500" : ""}
              />
              {errors.firstName && <p className="text-xs text-red-600">{errors.firstName}</p>}
            </div>

            {/* Last Name */}
            <div className="space-y-2">
              <Label htmlFor="lastName" className="text-sm font-medium text-zinc-700">
                Last name
              </Label>
              <Input
                id="lastName"
                type="text"
                placeholder="e.g. Cooper"
                value={formData.lastName}
                onChange={(e) => handleInputChange("lastName", e.target.value)}
                className={errors.lastName ? "border-red-300 focus:border-red-500 focus:ring-red-500" : ""}
              />
              {errors.lastName && <p className="text-xs text-red-600">{errors.lastName}</p>}
            </div>

            {/* YouTube URL */}
            <div className="space-y-2">
              <Label htmlFor="youtubeUrl" className="text-sm font-medium text-zinc-700">
                YouTube URL
              </Label>
              <Input
                id="youtubeUrl"
                type="url"
                placeholder="https://youtube.com/watch?v=..."
                value={formData.youtubeUrl}
                onChange={(e) => handleInputChange("youtubeUrl", e.target.value)}
                className={errors.youtubeUrl ? "border-red-300 focus:border-red-500 focus:ring-red-500" : ""}
              />
              {errors.youtubeUrl && <p className="text-xs text-red-600">{errors.youtubeUrl}</p>}
              <p className="text-xs text-zinc-500">Link to a video where the builder explains their AI workflow</p>
            </div>
          </div>

          <DialogFooter className="flex items-center justify-between pt-4">
            <Link
              href="/how-it-works"
              target="_blank"
              className="text-xs text-zinc-500 hover:text-zinc-700 flex items-center gap-1"
            >
              How it Works
              <ExternalLink className="size-3" />
            </Link>

            <div className="flex gap-3">
              <Button type="button" variant="ghost" onClick={onClose} disabled={isSubmitting}>
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting} className="bg-zinc-900 hover:bg-zinc-800">
                {isSubmitting ? "Adding..." : "Add Builder"}
              </Button>
            </div>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
