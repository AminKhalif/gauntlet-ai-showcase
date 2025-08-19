"""Plans optimal audio chunks and creates chunk files for parallel processing.

Takes: Audio file path and chunking parameters
Outputs: List of ChunkTimestamp objects and created audio chunk files
Used by: full_transcript_orchestrator.py to prepare audio for parallel transcription
"""

from pathlib import Path
from typing import List

from backend_app.models.audio_chunker_models import ChunkTimestamp
from backend_app.services.ffmpeg_audio_splitter import (
    get_audio_duration_seconds,
    calculate_chunk_timestamps,
    create_audio_chunk
)


def plan_audio_chunks(
    audio_file_path: str,
    chunk_duration: int = 480,
    overlap: int = 30
) -> List[ChunkTimestamp]:
    """Plan chunk timestamps for audio file.
    
    Args:
        audio_file_path: Path to audio file
        chunk_duration: Duration of each chunk in seconds
        overlap: Overlap between chunks in seconds
        
    Returns:
        List of ChunkTimestamp objects
        
    Raises:
        ValueError: If audio file cannot be processed
    """
    total_duration = get_audio_duration_seconds(audio_file_path)
    return calculate_chunk_timestamps(total_duration, chunk_duration, overlap)


def create_all_chunk_files(
    audio_file_path: str,
    chunk_timestamps: List[ChunkTimestamp],
    output_dir: str
) -> List[str]:
    """Create all audio chunk files from timestamps.
    
    Args:
        audio_file_path: Path to original audio file
        chunk_timestamps: List of chunk timing information
        output_dir: Directory for chunk outputs
        
    Returns:
        List of chunk audio file paths
        
    Raises:
        ValueError: If chunk creation fails
    """
    chunks_dir = Path(output_dir) / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    
    chunk_paths = []
    for timestamp in chunk_timestamps:
        chunk_path = chunks_dir / f"audio_chunk_{timestamp.chunk_number:03d}.mp3"
        create_audio_chunk(audio_file_path, str(chunk_path), timestamp)
        chunk_paths.append(str(chunk_path))
    
    return chunk_paths


def validate_chunk_files(chunk_paths: List[str]) -> bool:
    """Validate that all chunk files exist and are valid audio.
    
    Args:
        chunk_paths: List of chunk file paths to validate
        
    Returns:
        True if all chunks are valid
        
    Raises:
        ValueError: If any chunk is invalid with details
    """
    for chunk_path in chunk_paths:
        path_obj = Path(chunk_path)
        
        if not path_obj.exists():
            raise ValueError(f"Chunk file missing: {chunk_path}")
        
        try:
            duration = get_audio_duration_seconds(chunk_path)
            if duration <= 0:
                raise ValueError(f"Chunk has invalid duration: {chunk_path}")
        except Exception as e:
            raise ValueError(f"Chunk is not valid audio: {chunk_path} - {e}")
    
    return True