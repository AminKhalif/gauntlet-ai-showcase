"""Gemini API service for role-aware audio diarization using Files API."""

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


def inspect_empty_response(response: Any) -> str:
    """Inspect empty response from Gemini to provide diagnostic information.
    
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


def generate_role_aware_transcript(uploaded_file: Any, max_retries: int = 2) -> str:
    """Generate role-aware diarized transcript from uploaded audio file.
    
    Args:
        uploaded_file: Gemini File object representing the uploaded audio
        max_retries: Maximum number of retries for empty responses
        
    Returns:
        Role-aware diarized transcript as a string
        
    Raises:
        ValueError: If transcript generation fails after retries
    """
    client = get_gemini_client()
    
    # Prompt for role-aware diarized transcription
    prompt = """Please transcribe this podcast audio and provide a role-aware diarized transcript. 

This is a podcast interview between two speakers:
- An INTERVIEWER who asks questions
- An INTERVIEWEE (builder/developer) who explains their AI workflow and development techniques

Your task:
1. Use both voice characteristics AND content analysis to identify speakers
2. Label each segment as either "Interviewer:" or "Interviewee:" 
3. Maintain consistent labeling throughout the entire episode
4. Include timestamps in [MM:SS] format

Analysis guidelines:
- The INTERVIEWER typically asks questions, guides conversation, introduces topics
- The INTERVIEWEE typically provides detailed technical explanations, describes their workflow, explains tools and techniques
- Use voice characteristics to distinguish speakers, but prioritize conversational role consistency

Format:
Interviewer: [MM:SS] [question or guidance text]
Interviewee: [MM:SS] [technical explanation or answer]

Focus on accuracy and maintaining consistent speaker roles throughout the conversation."""
    
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            # Generate content using new SDK
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[prompt, uploaded_file]
            )
            
            if response.text and response.text.strip():
                return response.text
            
            # Empty response - inspect and retry if attempts remaining
            diagnostics = inspect_empty_response(response)
            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
                continue
            else:
                raise ValueError(f"No transcript generated from audio after retries. Response details: {diagnostics}")
                
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                raise ValueError(f"Failed to generate role-aware transcript: {e}")


def process_podcast_for_role_diarization(
    audio_file_path: str, 
    output_file_path: str,
    display_name: Optional[str] = None
) -> str:
    """Complete pipeline: upload podcast to Gemini and generate role-aware diarized transcript.
    
    Args:
        audio_file_path: Path to the input podcast audio file
        output_file_path: Path where the transcript should be saved
        display_name: Optional display name for the uploaded file
        
    Returns:
        Path to the saved transcript file
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If processing fails
    """
    # Upload audio file
    uploaded_file = upload_audio_to_gemini(audio_file_path, display_name)
    
    try:
        # Wait for file processing before using it
        client = get_gemini_client()
        wait_for_file_processing(client, uploaded_file.name)
        
        # Generate role-aware diarized transcript
        transcript = generate_role_aware_transcript(uploaded_file)
        
        # Save transcript to file
        output_path = Path(output_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        return str(output_path)
        
    finally:
        # Clean up uploaded file - new SDK uses client
        try:
            client = get_gemini_client()
            client.files.delete(uploaded_file.name)
        except Exception:
            # Ignore cleanup errors
            pass