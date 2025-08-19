"""Transcribes individual audio chunks using Gemini API with absolute timestamps.

Takes: Audio chunk files (.mp3) + chunk timing info (ChunkTimestamp)
Outputs: Individual transcript files with speaker labels and timestamps  
Used by: full_transcript_orchestrator.py for parallel chunk processing
"""

import asyncio
from dataclasses import dataclass

from backend_app.models.audio_chunker_models import ChunkTimestamp
from backend_app.services.gemini_api_client import (
    upload_audio_to_gemini,
    wait_for_file_processing,
    get_gemini_client,
    inspect_gemini_response
)


@dataclass(frozen=True)
class TranscriptResult:
    """Result of transcribing a single chunk."""
    chunk_number: int
    start_seconds: int
    end_seconds: int
    transcript_text: str


def create_chunk_transcript_prompt(chunk_timestamp: ChunkTimestamp) -> str:
    """Create prompt for chunk transcription with absolute timestamps.
    
    Args:
        chunk_timestamp: Timing information for this chunk
        
    Returns:
        Formatted prompt string for Gemini
    """
    start_mm_ss = f"{chunk_timestamp.start_seconds // 60:02d}:{chunk_timestamp.start_seconds % 60:02d}"
    end_mm_ss = f"{chunk_timestamp.end_seconds // 60:02d}:{chunk_timestamp.end_seconds % 60:02d}"
    
    return f"""Transcribe ALL spoken words in this audio chunk with speaker labels and timestamps.

Audio segment: {start_mm_ss} to {end_mm_ss} of full episode.

MANDATORY REQUIREMENTS:
1. Transcribe EVERY SINGLE SPOKEN WORD until {end_mm_ss} - do NOT stop early
2. Transcribe ALL speech regardless of topic - conversations, questions, answers, side comments, everything
3. EVERY LINE must start with "Interviewer:" or "Interviewee:" - NO EXCEPTIONS
4. Use absolute timestamps from full episode (starting {start_mm_ss})
5. Continue transcribing past apparent endings like "thank you" or "goodbye"

CRITICAL FORMATTING - EVERY line must look exactly like this:
✓ Interviewer: [MM:SS] exact words spoken
✓ Interviewee: [MM:SS] exact words spoken
✗ [MM:SS] words without speaker label ← NEVER DO THIS

IGNORE ONLY: background sounds, music, crying, non-speech audio

CRITICAL: Your final timestamp must reach very close to {end_mm_ss}. The audio contains speech throughout the entire duration."""


async def transcribe_audio_chunk(
    chunk_timestamp: ChunkTimestamp,
    chunk_audio_path: str
) -> TranscriptResult:
    """Transcribe single audio chunk using fresh Gemini client.
    
    Args:
        chunk_timestamp: Timing information for this chunk
        chunk_audio_path: Path to chunk audio file
        
    Returns:
        TranscriptResult with transcript text
        
    Raises:
        ValueError: If transcription fails after retry
    """
    # Create fresh client for this chunk to avoid thread safety issues
    client = get_gemini_client()
    
    # Upload and wait for processing
    uploaded_file = await asyncio.get_event_loop().run_in_executor(
        None, upload_audio_to_gemini, chunk_audio_path
    )
    
    await asyncio.get_event_loop().run_in_executor(
        None, wait_for_file_processing, client, uploaded_file.name
    )
    
    # Generate transcript with absolute timestamps
    prompt = create_chunk_transcript_prompt(chunk_timestamp)
    
    # Generate content with retry
    max_retries = 1
    chunk_num = chunk_timestamp.chunk_number
    
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, uploaded_file]
            )
            
            if response.text and response.text.strip():
                transcript_text = response.text.strip()
                break
                
            if attempt < max_retries:
                import time
                time.sleep(2 ** attempt)
                continue
            else:
                diagnostics = inspect_gemini_response(response)
                raise ValueError(f"Empty response from Gemini for chunk {chunk_num}. Details: {diagnostics}")
                
        except Exception as e:
            if attempt < max_retries:
                import time
                time.sleep(2 ** attempt)
                continue
            else:
                start_mm_ss = f"{chunk_timestamp.start_seconds // 60:02d}:{chunk_timestamp.start_seconds % 60:02d}"
                end_mm_ss = f"{chunk_timestamp.end_seconds // 60:02d}:{chunk_timestamp.end_seconds % 60:02d}"
                raise ValueError(f"Chunk {chunk_num} ({start_mm_ss}-{end_mm_ss}) failed: {e}")
    
    # Clean up uploaded file
    try:
        await asyncio.get_event_loop().run_in_executor(
            None, client.files.delete, uploaded_file.name
        )
    except Exception:
        pass  # Ignore cleanup errors
        
    return TranscriptResult(
        chunk_number=chunk_num,
        start_seconds=chunk_timestamp.start_seconds,
        end_seconds=chunk_timestamp.end_seconds,
        transcript_text=transcript_text
    )