"""Data models for audio chunking operations."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ChunkTimestamp:
    """Represents a single audio chunk's time boundaries.
    
    Args:
        start_seconds: Start time in seconds
        end_seconds: End time in seconds
        chunk_number: Sequential chunk number (1-based)
    """
    start_seconds: int
    end_seconds: int
    chunk_number: int


@dataclass(frozen=True)
class AudioChunkRequest:
    """Request to chunk an audio file.
    
    Args:
        gcs_blob_name: Name of audio file in GCS bucket
        bucket_name: GCS bucket name (optional, uses env default)
        chunk_duration_seconds: Length of each chunk in seconds
        overlap_seconds: Overlap between chunks in seconds
    """
    gcs_blob_name: str
    bucket_name: str | None = None
    chunk_duration_seconds: int = 480  # 8 minutes
    overlap_seconds: int = 30  # 30 seconds


@dataclass(frozen=True)
class AudioChunkResult:
    """Result of audio chunking operation.
    
    Args:
        job_id: Unique identifier for this chunking job
        original_blob_name: Original audio file name
        chunk_blob_names: List of generated chunk file names
        total_chunks: Number of chunks created
        total_duration_seconds: Duration of original audio in seconds
    """
    job_id: str
    original_blob_name: str
    chunk_blob_names: List[str]
    total_chunks: int
    total_duration_seconds: int


@dataclass(frozen=True)
class ChunkingProgress:
    """Progress tracking for chunking operation.
    
    Args:
        job_id: Unique identifier for this chunking job
        status: Current status (downloading, chunking, uploading, completed, failed)
        progress_percent: Progress percentage (0-100)
        current_step: Human-readable current step
        chunks_completed: Number of chunks processed
        total_chunks: Total number of chunks to process
        error_message: Error message if status is failed
    """
    job_id: str
    status: str
    progress_percent: int
    current_step: str
    chunks_completed: int = 0
    total_chunks: int = 0
    error_message: str | None = None