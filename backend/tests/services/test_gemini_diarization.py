"""Tests for Gemini API audio diarization service."""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append('src')
from backend_app.services.gemini_diarization import (
    get_gemini_client,
    upload_audio_to_gemini,
    generate_role_aware_transcript,
    process_podcast_for_role_diarization
)


def test_process_podcast_for_role_diarization_integration():
    """
    Integration test for the complete podcast diarization pipeline.
    
    This test uses the MP3 file in tests/downloads/ folder. The audio file can be obtained 
    in multiple ways:
    1. Already present in downloads folder (for development/testing)
    2. Downloaded using our YouTube downloader service (see test_youtube_downloader.py)
    3. Any other ~1 hour podcast audio file for testing purposes
    
    The test writes the transcript to tests/downloads/transcript.txt for review.
    """
    # Path to test audio file in downloads folder
    audio_file_path = "tests/downloads/AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3"
    
    # Output transcript to downloads folder as requested
    output_transcript_path = "tests/downloads/transcript.txt"
    
    # Skip test if audio file doesn't exist (per downloads/README.md guidance)
    if not os.path.exists(audio_file_path):
        # Tests gracefully handle missing audio files as per downloads README
        # To run this test: use youtube_downloader.py or add your own ~1 hour audio file
        pytest.skip("Audio file not found - see tests/downloads/README.md for setup instructions")
        return
    
    # Verify GEMINI_API_KEY is available
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY environment variable not set")
        return
    
    try:
        # Run the complete diarization pipeline
        result_path = process_podcast_for_role_diarization(
            audio_file_path=audio_file_path,
            output_file_path=output_transcript_path,
            display_name="Test Podcast for Diarization"
        )
        
        # Verify transcript file was created
        assert os.path.exists(result_path)
        assert result_path == output_transcript_path
        
        # Verify transcript has content
        with open(result_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        assert len(transcript_content) > 0
        assert "Interviewer:" in transcript_content or "Interviewee:" in transcript_content
        
        print(f"✅ Transcript successfully generated at: {result_path}")
        print(f"📝 Transcript length: {len(transcript_content)} characters")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


def test_get_gemini_client_missing_api_key():
    """Test get_gemini_client raises error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        try:
            get_gemini_client()
            assert False, "Expected ValueError for missing API key"
        except ValueError as e:
            assert "GEMINI_API_KEY environment variable must be set" in str(e)


def test_upload_audio_to_gemini_file_not_found():
    """Test upload_audio_to_gemini raises error for non-existent file."""
    try:
        upload_audio_to_gemini("nonexistent_file.mp3")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as e:
        assert "Audio file not found" in str(e)


@patch('backend_app.services.gemini_diarization.get_gemini_client')
def test_generate_role_aware_transcript_success(mock_get_client):
    """Test successful transcript generation."""
    # Mock the response
    mock_response = Mock()
    mock_response.text = "Interviewer: [00:00] Welcome to the show!\nInterviewee: [00:05] Thanks for having me!"
    
    # Mock client and models
    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    # Mock uploaded file
    mock_file = Mock()
    
    result = generate_role_aware_transcript(mock_file)
    
    assert "Interviewer:" in result
    assert "Interviewee:" in result
    mock_client.models.generate_content.assert_called_once()


@patch('backend_app.services.gemini_diarization.get_gemini_client')
def test_generate_role_aware_transcript_empty_response(mock_get_client):
    """Test transcript generation with empty response."""
    mock_response = Mock()
    mock_response.text = ""
    
    # Mock client and models
    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    mock_file = Mock()
    
    try:
        generate_role_aware_transcript(mock_file)
        assert False, "Expected ValueError for empty response"
    except ValueError as e:
        assert "No transcript generated from audio" in str(e)