"""Service for merging overlapping transcript chunks."""

import re
from typing import List, Optional, Tuple

from backend_app.services.transcript_service import TranscriptResult


def extract_timestamp_seconds(line: str) -> Optional[int]:
    """Extract timestamp in seconds from transcript line.
    
    Args:
        line: Transcript line potentially containing [MM:SS] timestamp
        
    Returns:
        Timestamp in seconds, or None if no valid timestamp found
    """
    match = re.search(r'\[(\d{1,2}):(\d{2})\]', line)
    if match:
        minutes, seconds = map(int, match.groups())
        return minutes * 60 + seconds
    return None


def merge_transcript_chunks(
    transcript_results: List[TranscriptResult],
    tolerance_seconds: int = 2
) -> str:
    """Merge overlapping transcript chunks into final transcript.
    
    Args:
        transcript_results: List of transcript results, ordered by chunk_number
        tolerance_seconds: Tolerance for timestamp overlap handling
        
    Returns:
        Merged transcript as string
        
    Raises:
        ValueError: If transcript results are invalid
    """
    if not transcript_results:
        raise ValueError("No transcript results to merge")
    
    # Sort by chunk number to ensure correct order
    sorted_results = sorted(transcript_results, key=lambda x: x.chunk_number)
    merged_lines = []
    
    for i, result in enumerate(sorted_results):
        lines = result.transcript_text.strip().split('\n')
        
        if i == 0:
            # First chunk: add all lines
            merged_lines.extend(lines)
        else:
            # Subsequent chunks: drop overlapping lines
            prev_result_end = sorted_results[i-1].end_seconds
            cutoff_time = prev_result_end - tolerance_seconds
            
            for line in lines:
                line_timestamp = extract_timestamp_seconds(line)
                if line_timestamp is None or line_timestamp > cutoff_time:
                    merged_lines.append(line)
    
    return '\n'.join(merged_lines)


def remove_backwards_timestamps(transcript: str) -> str:
    """Remove lines with backwards timestamps from transcript.
    
    Args:
        transcript: Raw merged transcript
        
    Returns:
        Validated transcript with monotonic timestamps
    """
    lines = transcript.split('\n')
    validated_lines = []
    last_timestamp = -1
    
    for line in lines:
        line_timestamp = extract_timestamp_seconds(line)
        if line_timestamp is None:
            # Non-timestamped line, keep it
            validated_lines.append(line)
        elif line_timestamp >= last_timestamp:
            # Timestamp is in order
            validated_lines.append(line)
            last_timestamp = line_timestamp
        # Drop lines with backwards timestamps silently
    
    return '\n'.join(validated_lines)


def validate_transcript_completeness(
    transcript: str,
    expected_duration_seconds: int,
    tolerance_seconds: int = 30
) -> Tuple[bool, str]:
    """Validate completeness of final merged transcript.
    
    Args:
        transcript: Final merged transcript
        expected_duration_seconds: Expected total duration
        tolerance_seconds: Acceptable difference from expected duration
        
    Returns:
        Tuple of (is_valid, validation_message)
    """
    lines = transcript.strip().split('\n')
    last_timestamp = None
    
    # Find last timestamp in transcript
    for line in reversed(lines):
        timestamp = extract_timestamp_seconds(line)
        if timestamp is not None:
            last_timestamp = timestamp
            break
    
    if last_timestamp is None:
        return False, "No timestamps found in final transcript"
    
    expected_min = expected_duration_seconds - tolerance_seconds
    if last_timestamp >= expected_min:
        return True, f"Complete: final timestamp {last_timestamp}s (expected ~{expected_duration_seconds}s)"
    else:
        missing_time = expected_duration_seconds - last_timestamp
        return False, f"Incomplete: final timestamp {last_timestamp}s, missing ~{missing_time}s from expected {expected_duration_seconds}s"


def process_transcript_merge(
    transcript_results: List[TranscriptResult],
    expected_duration_seconds: int
) -> str:
    """Complete transcript merge with validation.
    
    Args:
        transcript_results: List of transcript results to merge
        expected_duration_seconds: Expected total audio duration
        
    Returns:
        Final validated transcript
        
    Raises:
        ValueError: If merge fails or validation fails
    """
    # Merge overlapping chunks
    merged_transcript = merge_transcript_chunks(transcript_results)
    
    # Remove backwards timestamps
    validated_transcript = remove_backwards_timestamps(merged_transcript)
    
    # Validate completeness
    is_valid, validation_msg = validate_transcript_completeness(
        validated_transcript, expected_duration_seconds
    )
    if not is_valid:
        raise ValueError(f"Transcript validation failed: {validation_msg}")
    
    return validated_transcript