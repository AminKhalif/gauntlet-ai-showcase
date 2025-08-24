"""FastAPI routes for builder CRUD operations.

Takes: HTTP requests with builder data
Outputs: JSON responses with builder records and status codes
Used by: Next.js frontend API routes for builder management

Handles all builder-related endpoints with proper error handling and validation.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
import re

from backend_app.services.supabase_builder_writer import (
    create_builder_record,
    get_builder_by_slug,
    mark_builder_status
)

router = APIRouter(prefix="/api/builders", tags=["builders"])


class CreateBuilderRequest(BaseModel):
    """Request model for creating a new builder."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50) 
    youtube_url: str = Field(..., min_length=10, max_length=500)
    
    @validator('youtube_url')
    def validate_youtube_url(cls, url: str) -> str:
        """Validate YouTube URL format."""
        youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if not re.match(youtube_pattern, url):
            raise ValueError('Invalid YouTube URL format')
        return url


class CreateBuilderResponse(BaseModel):
    """Response model for builder creation."""
    success: bool
    builder_id: str
    slug: str
    message: str


class BuilderProfileResponse(BaseModel):
    """Response model for builder profile data."""
    builder: dict
    workflow_cards: dict


def create_slug_from_name(first_name: str, last_name: str) -> str:
    """Generate URL-friendly slug from builder name.
    
    Args:
        first_name: Builder's first name
        last_name: Builder's last name
        
    Returns:
        URL-friendly slug (e.g., "jane-cooper")
    """
    full_name = f"{first_name} {last_name}"
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', full_name)  # Remove special chars
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'-+', '-', slug)  # Replace multiple hyphens
    return slug.lower().strip('-')


@router.post("/", response_model=CreateBuilderResponse)
async def create_builder(request: CreateBuilderRequest) -> CreateBuilderResponse:
    """Create a new builder record.
    
    Args:
        request: Builder creation data
        
    Returns:
        Created builder information
        
    Raises:
        HTTPException: If creation fails or validation errors
    """
    try:
        full_name = f"{request.first_name} {request.last_name}"
        slug = create_slug_from_name(request.first_name, request.last_name)
        
        # Check if slug already exists
        existing_builder = get_builder_by_slug(slug)
        if existing_builder:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Builder with name '{full_name}' already exists"
            )
        
        # Create builder record
        builder_id = create_builder_record(
            name=full_name,
            slug=slug,
            youtube_url=request.youtube_url
        )
        
        return CreateBuilderResponse(
            success=True,
            builder_id=builder_id,
            slug=slug,
            message=f"Builder '{full_name}' created successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create builder: {str(e)}"
        )


@router.get("/{slug}", response_model=BuilderProfileResponse)
async def get_builder_profile(slug: str) -> BuilderProfileResponse:
    """Get complete builder profile by slug.
    
    Args:
        slug: URL-friendly builder identifier
        
    Returns:
        Complete builder profile with workflow cards
        
    Raises:
        HTTPException: If builder not found or query fails
    """
    try:
        builder_profile = get_builder_by_slug(slug)
        
        if not builder_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Builder with slug '{slug}' not found"
            )
        
        return BuilderProfileResponse(
            builder=builder_profile['builder'],
            workflow_cards=builder_profile['workflow_cards']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve builder profile: {str(e)}"
        )


@router.patch("/{slug}/status")
async def update_builder_status(
    slug: str, 
    status_value: str,
    error_message: Optional[str] = None
) -> dict:
    """Update builder processing status.
    
    Args:
        slug: URL-friendly builder identifier
        status_value: New status (pending, processing, completed, failed)
        error_message: Optional error details if status is 'failed'
        
    Returns:
        Success confirmation
        
    Raises:
        HTTPException: If builder not found or update fails
    """
    try:
        # Get builder to verify it exists
        builder_profile = get_builder_by_slug(slug)
        if not builder_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Builder with slug '{slug}' not found"
            )
        
        builder_id = builder_profile['builder']['id']
        
        # Update status
        mark_builder_status(builder_id, status_value, error_message)
        
        return {
            "success": True,
            "message": f"Builder status updated to '{status_value}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update builder status: {str(e)}"
        )