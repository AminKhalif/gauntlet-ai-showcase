"""Supabase database writer for builder workflow data.

Takes: Builder information and workflow card data
Outputs: Database records with generated UUIDs
Used by: API endpoints and pipeline orchestration for data persistence

Handles all CRUD operations for builders, workflow cards, and processing jobs.
"""

import os
from typing import Any, Dict, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

from backend_app.models.workflow_card_models import WorkflowCardsOutput

load_dotenv()


def get_supabase_client() -> Client:
    """Get authenticated Supabase client with service role key.
    
    Returns:
        Authenticated Supabase client for database operations
        
    Raises:
        ValueError: If environment variables are missing
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment")
    
    return create_client(url, key)


def create_builder_record(name: str, slug: str, youtube_url: str, avatar_url: Optional[str] = None) -> str:
    """Create new builder record in database.
    
    Args:
        name: Full name of the builder
        slug: URL-friendly identifier (e.g., "jane-cooper" from "Jane Cooper")
        youtube_url: Original YouTube video URL
        avatar_url: Optional avatar image URL
        
    Returns:
        UUID string of the created builder record
        
    Raises:
        Exception: If database operation fails
    """
    client = get_supabase_client()
    
    builder_data = {
        "name": name,
        "slug": slug,
        "youtube_url": youtube_url,
        "avatar_url": avatar_url,
        "status": "pending"
    }
    
    response = client.table("builders").insert(builder_data).execute()
    
    if not response.data:
        raise Exception("Failed to create builder record")
    
    return response.data[0]["id"]


def save_audio_metadata(
    builder_id: str, 
    gcs_blob_name: str, 
    gcs_url: str, 
    duration_seconds: Optional[float] = None
) -> None:
    """Update builder record with GCS audio file metadata.
    
    Args:
        builder_id: UUID of the builder record
        gcs_blob_name: GCS blob path/name
        gcs_url: Public GCS URL for the audio file
        duration_seconds: Length of audio in seconds
        
    Raises:
        Exception: If database update fails
    """
    client = get_supabase_client()
    
    update_data = {
        "gcs_audio_blob_name": gcs_blob_name,
        "gcs_audio_url": gcs_url,
        "audio_duration_seconds": duration_seconds,
        "status": "processing"
    }
    
    response = client.table("builders").update(update_data).eq("id", builder_id).execute()
    
    if not response.data:
        raise Exception(f"Failed to update builder {builder_id} with audio metadata")


def save_workflow_cards(builder_id: str, workflow_cards: WorkflowCardsOutput) -> None:
    """Save extracted workflow cards to database.
    
    Args:
        builder_id: UUID of the builder record
        workflow_cards: Complete workflow card data from LangExtract
        
    Raises:
        Exception: If database operation fails
    """
    client = get_supabase_client()
    
    # Convert WorkflowCardsOutput to database records
    card_types = [
        ("planning_scoping", workflow_cards.planning_scoping),
        ("context_management", workflow_cards.context_management),
        ("codegen_loop", workflow_cards.codegen_loop),
        ("verification_safeguards", workflow_cards.verification_safeguards),
        ("iteration_style", workflow_cards.iteration_style),
        ("deployment_delivery", workflow_cards.deployment_delivery)
    ]
    
    rows = []
    for card_type, card_data in card_types:
        rows.append({
            "builder_id": builder_id,
            "card_type": card_type,
            "summary": card_data.summary,
            "workflow_json": card_data.dict()  # Store full WorkflowCard as JSON
        })
    
    if rows:
        response = client.table("workflow_cards").upsert(
            rows, 
            on_conflict="builder_id,card_type"
        ).execute()
        
        if not response.data:
            raise Exception(f"Failed to save workflow cards for builder {builder_id}")


def mark_builder_status(builder_id: str, status: str, error_message: Optional[str] = None) -> None:
    """Update builder processing status.
    
    Args:
        builder_id: UUID of the builder record
        status: New status (pending, processing, completed, failed)
        error_message: Optional error details if status is 'failed'
        
    Raises:
        Exception: If database update fails
    """
    client = get_supabase_client()
    
    update_data = {"status": status}
    if error_message:
        update_data["error_message"] = error_message
    
    response = client.table("builders").update(update_data).eq("id", builder_id).execute()
    
    if not response.data:
        raise Exception(f"Failed to update builder {builder_id} status to {status}")


def get_builder_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """Retrieve complete builder profile by URL slug.
    
    Args:
        slug: URL-friendly builder identifier (e.g., "jane-cooper")
        
    Returns:
        Dict with builder data and workflow cards, or None if not found
        
    Raises:
        Exception: If database query fails
    """
    client = get_supabase_client()
    
    # Get builder record
    builder_response = client.table("builders").select("*").eq("slug", slug).execute()
    
    if not builder_response.data:
        return None
    
    builder = builder_response.data[0]
    
    # Get workflow cards for this builder
    cards_response = client.table("workflow_cards").select("*").eq("builder_id", builder["id"]).execute()
    
    # Organize cards by type
    workflow_cards = {}
    if cards_response.data:
        for card in cards_response.data:
            workflow_cards[card["card_type"]] = card["workflow_json"]
    
    return {
        "builder": builder,
        "workflow_cards": workflow_cards
    }


def create_processing_job(builder_id: str) -> str:
    """Create a processing job record for status tracking.
    
    Args:
        builder_id: UUID of the builder record
        
    Returns:
        UUID of the created processing job
        
    Raises:
        Exception: If database operation fails
    """
    client = get_supabase_client()
    
    job_data = {
        "builder_id": builder_id,
        "status": "pending",
        "current_stage": "initializing",
        "progress_percentage": 0
    }
    
    response = client.table("processing_jobs").insert(job_data).execute()
    
    if not response.data:
        raise Exception("Failed to create processing job")
    
    return response.data[0]["id"]


def update_processing_job(
    job_id: str, 
    status: Optional[str] = None,
    stage: Optional[str] = None,
    progress: Optional[int] = None,
    error_message: Optional[str] = None
) -> None:
    """Update processing job status and progress.
    
    Args:
        job_id: UUID of the processing job
        status: New status (pending, processing, completed, failed)
        stage: Current processing stage description
        progress: Progress percentage (0-100)
        error_message: Error details if status is 'failed'
        
    Raises:
        Exception: If database update fails
    """
    client = get_supabase_client()
    
    update_data = {}
    if status is not None:
        update_data["status"] = status
    if stage is not None:
        update_data["current_stage"] = stage
    if progress is not None:
        update_data["progress_percentage"] = progress
    if error_message is not None:
        update_data["error_message"] = error_message
    
    if status == "completed":
        update_data["completed_at"] = "now()"
    
    response = client.table("processing_jobs").update(update_data).eq("id", job_id).execute()
    
    if not response.data:
        raise Exception(f"Failed to update processing job {job_id}")