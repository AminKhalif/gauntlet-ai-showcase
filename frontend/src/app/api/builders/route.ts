/**
 * @fileoverview Next.js API route for builder CRUD operations via FastAPI.
 */

import { NextRequest, NextResponse } from "next/server"

type CreateBuilderRequest = {
  firstName: string
  lastName: string
  youtubeUrl: string
}

type CreateBuilderResponse = {
  success: boolean
  builder_id: string
  slug: string
  message: string
}

const FASTAPI_BASE_URL = process.env.NEXT_PUBLIC_FASTAPI_BASE_URL || "http://localhost:8001"

/**
 * @description Creates a new builder by calling FastAPI backend.
 */
export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body: CreateBuilderRequest = await request.json()

    // Transform to FastAPI format
    const fastApiPayload = {
      first_name: body.firstName,
      last_name: body.lastName,
      youtube_url: body.youtubeUrl,
    }

    // Call FastAPI backend
    const response = await fetch(`${FASTAPI_BASE_URL}/api/builders/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(fastApiPayload),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        detail: "Unknown error occurred"
      }))
      
      return NextResponse.json(
        { error: errorData.detail || "Failed to create builder" },
        { status: response.status }
      )
    }

    const result: CreateBuilderResponse = await response.json()
    return NextResponse.json(result)

  } catch (error) {
    console.error("API Error:", error)
    
    if (error instanceof Error && error.message.includes("fetch")) {
      return NextResponse.json(
        { error: "Cannot connect to backend server. Is it running on localhost:8001?" },
        { status: 503 }
      )
    }

    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}