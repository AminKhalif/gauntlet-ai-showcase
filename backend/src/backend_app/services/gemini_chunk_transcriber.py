"""Transcribes individual audio chunks using Gemini API with absolute timestamps.

Takes: Audio chunk files (.mp3) + chunk timing info (ChunkTimestamp)
Outputs: Individual transcript files with speaker labels and timestamps  
Used by: full_transcript_orchestrator.py for parallel chunk processing
"""

import asyncio
import re
from dataclasses import dataclass
from typing import Optional

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


def validate_transcript_quality(
    transcript_text: str, 
    chunk_timestamp: ChunkTimestamp
) -> Optional[str]:
    """Validate transcript meets quality requirements.
    
    Args:
        transcript_text: Generated transcript to validate
        chunk_timestamp: Expected timing information
        
    Returns:
        Error message if validation fails, None if valid
    """
    # Check minimum length (should have substantial content)
    if len(transcript_text) < 100:
        return f"Transcript too short: {len(transcript_text)} chars (minimum 100)"
    
    # Check for proper speaker labels
    lines = transcript_text.strip().split('\n')
    valid_lines = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(('Interviewer:', 'Interviewee:')):
            valid_lines += 1
        else:
            return f"Invalid speaker label format: '{line[:50]}...'"
    
    if valid_lines == 0:
        return "No valid speaker-labeled lines found"
    
    # Extract final timestamp to check coverage
    final_timestamp = extract_final_timestamp_seconds(transcript_text)
    if final_timestamp is None:
        return "No valid timestamps found in transcript"
    
    # Check if transcript covers reasonable portion of chunk
    expected_end = chunk_timestamp.end_seconds
    coverage_threshold = 0.7  # Should cover at least 70% of chunk
    min_expected_timestamp = chunk_timestamp.start_seconds + (
        (expected_end - chunk_timestamp.start_seconds) * coverage_threshold
    )
    
    if final_timestamp < min_expected_timestamp:
        return f"Transcript ends too early: {final_timestamp}s vs expected >{min_expected_timestamp}s"
    
    return None  # Valid


def extract_final_timestamp_seconds(transcript_text: str) -> Optional[int]:
    """Extract the last timestamp from transcript in seconds.
    
    Args:
        transcript_text: Transcript content with timestamps
        
    Returns:
        Final timestamp in seconds, or None if no timestamps found
    """
    timestamp_pattern = r'\[(\d{2}):(\d{2})\]'
    matches = re.findall(timestamp_pattern, transcript_text)
    
    if not matches:
        return None
    
    # Get last timestamp
    last_match = matches[-1]
    minutes, seconds = int(last_match[0]), int(last_match[1])
    return minutes * 60 + seconds


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
    
    # Generate content with retry and validation
    max_retries = 3
    chunk_num = chunk_timestamp.chunk_number
    
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, uploaded_file]
            )
            
            if response.text and response.text.strip():
                transcript_text = response.text.strip()
                
                # Validate transcript quality
                validation_error = validate_transcript_quality(transcript_text, chunk_timestamp)
                
                if not validation_error:
                    break  # Success!
                elif attempt < max_retries:
                    # Validation failed, retry
                    import time
                    time.sleep(2 ** attempt)
                    continue
                else:
                    start_mm_ss = f"{chunk_timestamp.start_seconds // 60:02d}:{chunk_timestamp.start_seconds % 60:02d}"
                    end_mm_ss = f"{chunk_timestamp.end_seconds // 60:02d}:{chunk_timestamp.end_seconds % 60:02d}"
                    diagnostics = inspect_gemini_response(response)
                    raise ValueError(f"Chunk {chunk_num} ({start_mm_ss}-{end_mm_ss}) validation failed: {validation_error}. Response details: {diagnostics}")
                
            elif attempt < max_retries:
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