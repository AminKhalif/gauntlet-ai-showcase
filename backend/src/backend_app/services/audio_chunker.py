"""Audio chunking service for processing large audio files."""

import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import List

from backend_app.models.audio_chunker_models import (
    AudioChunkRequest, 
    AudioChunkResult, 
    ChunkTimestamp
)
from backend_app.services.gcs_storage import download_audio_file, upload_audio_file


def calculate_chunk_timestamps(
    total_duration_seconds: int, 
    chunk_duration: int = 480, 
    overlap: int = 30
) -> List[ChunkTimestamp]:
    """Calculate timestamp boundaries for audio chunks with overlaps.
    
    Args:
        total_duration_seconds: Total audio duration in seconds
        chunk_duration: Duration of each chunk in seconds (default 8 minutes)
        overlap: Overlap between chunks in seconds (default 30 seconds)
        
    Returns:
        List of ChunkTimestamp objects with start/end times
        
    Raises:
        ValueError: If parameters are invalid
    """
    if total_duration_seconds <= 0:
        raise ValueError("Total duration must be positive")
    if chunk_duration <= overlap:
        raise ValueError("Chunk duration must be greater than overlap")
    if overlap < 0:
        raise ValueError("Overlap cannot be negative")
        
    chunks = []
    chunk_number = 1
    current_start = 0
    
    while current_start < total_duration_seconds:
        # Calculate end time for this chunk
        current_end = min(current_start + chunk_duration, total_duration_seconds)
        
        chunks.append(ChunkTimestamp(
            start_seconds=current_start,
            end_seconds=current_end, 
            chunk_number=chunk_number
        ))
        
        # Move to next chunk start (accounting for overlap)
        next_start = current_start + chunk_duration - overlap
        
        # Break if next chunk would be too small or we've covered everything
        if next_start >= total_duration_seconds:
            break
            
        current_start = next_start
        chunk_number += 1
            
    return chunks


def get_audio_duration_seconds(file_path: str) -> int:
    """Get audio file duration in seconds using ffprobe.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Duration in seconds
        
    Raises:
        subprocess.CalledProcessError: If ffprobe command fails
        ValueError: If duration cannot be determined
    """
    if not Path(file_path).exists():
        raise ValueError(f"Audio file not found: {file_path}")
        
    try:
        result = subprocess.run([
            'ffprobe', '-i', file_path, 
            '-show_entries', 'format=duration',
            '-v', 'quiet', '-of', 'csv=p=0'
        ], capture_output=True, text=True, check=True)
        
        duration_str = result.stdout.strip()
        return int(float(duration_str))
        
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, f"ffprobe failed: {e.stderr}"
        )
    except (ValueError, IndexError) as e:
        raise ValueError(f"Could not parse audio duration: {e}")


def create_audio_chunk(
    input_path: str, 
    output_path: str, 
    timestamp: ChunkTimestamp
) -> None:
    """Create a single audio chunk using ffmpeg (no re-encoding).
    
    Args:
        input_path: Path to source audio file
        output_path: Path for output chunk file
        timestamp: Chunk timing information
        
    Raises:
        subprocess.CalledProcessError: If ffmpeg command fails
        ValueError: If paths are invalid
    """
    if not Path(input_path).exists():
        raise ValueError(f"Input file not found: {input_path}")
        
    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    duration = timestamp.end_seconds - timestamp.start_seconds
    
    try:
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-ss', str(timestamp.start_seconds),
            '-t', str(duration), 
            '-c', 'copy',  # No re-encoding for speed
            '-avoid_negative_ts', 'make_zero',
            '-y',  # Overwrite output file
            output_path
        ], check=True, capture_output=True)
        
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, f"ffmpeg chunking failed: {e.stderr}"
        )