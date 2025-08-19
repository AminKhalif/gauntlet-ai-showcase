"""Orchestrates complete audio-to-transcript pipeline with chunking and merging.

Takes: Full audio file (.mp3)
Outputs: Final merged transcript file with speaker labels and timestamps
Pipeline: Split audio → Transcribe chunks in parallel → Merge overlapping results
"""

import asyncio
from pathlib import Path

from backend_app.services.ffmpeg_audio_splitter import get_audio_duration_seconds
from backend_app.services.audio_chunk_planner import (
    plan_audio_chunks,
    create_all_chunk_files,
    validate_chunk_files
)
from backend_app.services.gemini_chunk_transcriber import transcribe_audio_chunk, TranscriptResult
from backend_app.services.chunk_transcript_merger import (
    process_transcript_merge,
    extract_timestamp_seconds,
    merge_chunk_transcripts,
    remove_backwards_timestamps as validate_timestamps_monotonic,
    validate_transcript_completeness
)
from backend_app.services.gemini_chunk_transcriber import TranscriptResult as ChunkTranscriptResult


def save_chunk_transcript(transcript_text: str, chunk_number: int, output_dir: str) -> str:
    """Save chunk transcript to file.
    
    Args:
        transcript_text: Transcript content to save
        chunk_number: Sequential chunk number
        output_dir: Directory for outputs
        
    Returns:
        Path to saved transcript file
    """
    chunks_dir = Path(output_dir) / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)
    
    transcript_path = chunks_dir / f"transcript_chunk_{chunk_number:03d}.txt"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    
    return str(transcript_path)


def save_final_transcript(transcript_text: str, output_dir: str) -> str:
    """Save final merged transcript to file.
    
    Args:
        transcript_text: Final merged transcript content
        output_dir: Directory for outputs
        
    Returns:
        Path to saved final transcript file
    """
    final_path = Path(output_dir) / "final_transcript.txt"
    final_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(final_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    
    return str(final_path)


async def process_audio_with_chunked_diarization(
    audio_file_path: str,
    output_dir: str = "backend/tests/downloads",
    max_concurrent: int = 3
) -> str:
    """Complete pipeline for chunked audio transcription with diarization.
    
    Args:
        audio_file_path: Path to input audio file
        output_dir: Directory for output files
        max_concurrent: Maximum concurrent chunk processing
        
    Returns:
        Path to final merged transcript file
        
    Raises:
        ValueError: If processing fails or validation fails
    """
    # Step 1: Plan chunks
    chunk_timestamps = plan_audio_chunks(audio_file_path)
    total_duration = get_audio_duration_seconds(audio_file_path)
    
    # Step 2: Create chunk audio files
    chunk_paths = create_all_chunk_files(audio_file_path, chunk_timestamps, output_dir)
    validate_chunk_files(chunk_paths)
    
    # Step 3: Transcribe chunks with limited concurrency
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single_chunk(timestamp, chunk_path):
        async with semaphore:
            # Each chunk gets its own fresh client to avoid thread safety issues
            transcript_result = await transcribe_audio_chunk(timestamp, chunk_path)
            
            # Save individual transcript
            transcript_path = save_chunk_transcript(
                transcript_result.transcript_text, 
                transcript_result.chunk_number, 
                output_dir
            )
            
            return transcript_result
    
    tasks = [
        process_single_chunk(timestamp, chunk_path)
        for timestamp, chunk_path in zip(chunk_timestamps, chunk_paths)
    ]
    
    transcript_results = await asyncio.gather(*tasks)
    
    # Step 4: Merge and validate transcripts
    final_transcript = process_transcript_merge(transcript_results, total_duration)
    
    # Step 5: Save final transcript
    final_path = save_final_transcript(final_transcript, output_dir)
    
    return final_path