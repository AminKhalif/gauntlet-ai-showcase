"""Basic Gemini API client utilities for file upload and processing.

Takes: Audio files for upload to Gemini Files API
Outputs: Uploaded file handles and API client instances
Used by: gemini_chunk_transcriber.py for individual chunk processing
"""

import os
import time
from pathlib import Path
from typing import Optional, Any
from google import genai
from dotenv import load_dotenv

load_dotenv()


def get_gemini_client() -> genai.Client:
    """Get configured Gemini client.
    
    Returns:
        Configured Gemini client
        
    Raises:
        ValueError: If GEMINI_API_KEY environment variable is not set
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable must be set")
    return genai.Client(api_key=api_key)


def wait_for_file_processing(
    client: genai.Client, 
    file_name: str, 
    max_wait_seconds: int = 300, 
    poll_interval_seconds: int = 5
) -> None:
    """Wait for uploaded file to be processed and ready for use.
    
    Args:
        client: Gemini client instance
        file_name: Name of the uploaded file to check
        max_wait_seconds: Maximum time to wait for processing (default: 5 minutes)
        poll_interval_seconds: Time between status checks (default: 5 seconds)
        
    Raises:
        TimeoutError: If file doesn't become ACTIVE within max_wait_seconds
        ValueError: If file processing fails with error details
    """
    start_time = time.time()
    
    while time.time() - start_time < max_wait_seconds:
        file_info = client.files.get(name=file_name)
        state = file_info.state
        
        if state == "ACTIVE":
            return
        elif state == "FAILED":
            error_msg = getattr(file_info, 'error', 'Unknown error')
            raise ValueError(f"File processing failed: {error_msg}")
        elif state in ("PROCESSING", "UPLOADING"):
            time.sleep(poll_interval_seconds)
        else:
            # Unexpected state, but continue polling in case it transitions
            time.sleep(poll_interval_seconds)
    
    raise TimeoutError(f"File {file_name} did not become ACTIVE within {max_wait_seconds} seconds")


def inspect_gemini_response(response: Any) -> str:
    """Inspect Gemini response to provide diagnostic information for debugging.
    
    Args:
        response: Gemini API response object
        
    Returns:
        Diagnostic string with response details for error messages
    """
    details = []
    
    # Check finish reason
    finish_reason = getattr(response, 'finish_reason', 'UNKNOWN')
    details.append(f"finish_reason='{finish_reason}'")
    
    # Check candidates
    candidates = getattr(response, 'candidates', [])
    details.append(f"candidates_count={len(candidates)}")
    
    if candidates:
        candidate = candidates[0]
        # Check if candidate has content
        content = getattr(candidate, 'content', None)
        if content:
            parts = getattr(content, 'parts', None)
            if parts is not None:
                details.append(f"content_parts={len(parts)}")
            else:
                details.append("content_parts=None")
        
        # Check for safety ratings or finish reason on candidate
        candidate_finish_reason = getattr(candidate, 'finish_reason', None)
        if candidate_finish_reason:
            details.append(f"candidate_finish_reason='{candidate_finish_reason}'")
            
        safety_ratings = getattr(candidate, 'safety_ratings', [])
        if safety_ratings:
            blocked_ratings = [r for r in safety_ratings if getattr(r, 'blocked', False)]
            if blocked_ratings:
                details.append(f"safety_blocked={len(blocked_ratings)}")
    
    # Check for usage metadata
    usage_metadata = getattr(response, 'usage_metadata', None)
    if usage_metadata:
        input_tokens = getattr(usage_metadata, 'prompt_token_count', 0)
        output_tokens = getattr(usage_metadata, 'candidates_token_count', 0)
        details.append(f"tokens_in={input_tokens},out={output_tokens}")
    
    return " | ".join(details)


def upload_audio_to_gemini(file_path: str, display_name: Optional[str] = None) -> Any:
    """Upload audio file to Gemini Files API.
    
    Args:
        file_path: Path to the audio file to upload
        display_name: Optional display name for the file
        
    Returns:
        Gemini File object representing the uploaded file
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ValueError: If file upload fails
    """
    client = get_gemini_client()
    
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    try:
        # Upload file to Gemini using new SDK
        uploaded_file = client.files.upload(file=file_path)
        return uploaded_file
        
    except Exception as e:
        raise ValueError(f"Failed to upload audio file to Gemini: {e}")




