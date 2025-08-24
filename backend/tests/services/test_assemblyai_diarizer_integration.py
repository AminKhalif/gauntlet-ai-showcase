"""Integration test for AssemblyAI diarization service.

SETUP INSTRUCTIONS (for new developers):
1. Use youtube_downloader.py to download any interview podcast
2. Use ffmpeg_audio_splitter.py to create small chunks (saves API credits)
3. Run this test with the first chunk (usually ~30 seconds)

This uses existing project services to create test data without burning API credits.
"""

import os
from pathlib import Path

import pytest

from backend_app.services.assemblyai_diarizer import transcribe_with_diarization, save_transcript_to_file


def test_transcribe_with_diarization_integration():
    """
    Integration test for AssemblyAI diarization with real API calls.
    
    Prerequisites:
    - Run youtube_downloader.py to get an interview MP3
    - Run ffmpeg_audio_splitter.py to create chunks/
    - Ensure ASSEMBLYAI_API_KEY is set in environment
    """
    # Look for existing audio chunks (created by ffmpeg_audio_splitter.py)
    chunks_dir = Path(__file__).parent.parent / "downloads" / "chunks"
    test_audio = chunks_dir / "audio_chunk_001.mp3"
    
    # Skip test with clear instructions if setup missing
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        pytest.skip("ASSEMBLYAI_API_KEY not set in environment variables")
    
    if not test_audio.exists():
        pytest.skip(
            f"Test audio chunk not found: {test_audio}\n"
            f"To create test data:\n"
            f"1. Run: uv run python src/backend_app/services/youtube_downloader.py\n"
            f"2. Run: uv run python src/backend_app/services/ffmpeg_audio_splitter.py\n"
            f"3. This will create chunks in {chunks_dir}"
        )
    
    # Test the transcription service
    result = transcribe_with_diarization(str(test_audio))
    
    # Validate expected output format
    assert isinstance(result, str)
    assert len(result) > 0
    assert "TRANSCRIPT WITH SPEAKER DIARIZATION" in result
    assert "Total duration:" in result
    assert "Number of speakers detected:" in result
    
    # Validate speaker role assignment
    assert "Interviewer" in result or "Interviewee" in result
    
    # Validate timestamp format [MM:SS - MM:SS]
    assert "[" in result and "]" in result
    
    # Test file saving functionality
    output_file = chunks_dir / "assemblyai_integration_test.txt"
    save_transcript_to_file(result, str(output_file))
    
    assert output_file.exists()
    saved_content = output_file.read_text()
    assert saved_content == result
    
    # Clean up test file
    output_file.unlink()


def test_transcribe_missing_file():
    """Test error handling for missing audio files."""
    with pytest.raises(FileNotFoundError):
        transcribe_with_diarization("nonexistent_file.mp3")


def test_transcribe_missing_api_key():
    """Test error handling for missing API key."""
    # Temporarily remove API key
    original_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if "ASSEMBLYAI_API_KEY" in os.environ:
        del os.environ["ASSEMBLYAI_API_KEY"]
    
    try:
        with pytest.raises(ValueError, match="ASSEMBLYAI_API_KEY environment variable not set"):
            transcribe_with_diarization("dummy_file.mp3")
    finally:
        # Restore original key if it existed
        if original_key:
            os.environ["ASSEMBLYAI_API_KEY"] = original_key