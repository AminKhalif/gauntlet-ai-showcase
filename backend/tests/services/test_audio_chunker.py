"""Tests for audio chunker service.

For integration tests that use real audio files:
- Place MP3 files in tests/downloads/ directory
- Or use the YouTube downloader service to get test files:
  Example: "AI for Software Engineers: The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3"
  YouTube URL: https://www.youtube.com/watch?v=YOUR_VIDEO_ID
"""

import os
import tempfile
from pathlib import Path

import pytest
from backend_app.services.audio_chunker import (
    calculate_chunk_timestamps,
    get_audio_duration_seconds,
    create_audio_chunk
)


def test_chunk_calculation_basic():
    """Test basic chunk calculation with overlap."""
    chunks = calculate_chunk_timestamps(
        total_duration_seconds=1200,  # 20 minutes
        chunk_duration=480,           # 8 minutes  
        overlap=30                    # 30 seconds
    )
    
    assert len(chunks) == 3
    assert chunks[0].start_seconds == 0
    assert chunks[0].end_seconds == 480
    assert chunks[1].start_seconds == 450  # 480 - 30 overlap
    assert chunks[1].end_seconds == 930
    assert chunks[2].start_seconds == 900  # 930 - 30 overlap


def test_chunk_calculation_edge_cases():
    """Test edge cases that could break the algorithm."""
    # Invalid inputs
    with pytest.raises(ValueError):
        calculate_chunk_timestamps(0, 480, 30)  # Zero duration
    
    with pytest.raises(ValueError):
        calculate_chunk_timestamps(1000, 30, 30)  # Chunk <= overlap
    
    # Very short audio
    chunks = calculate_chunk_timestamps(100, 480, 30)
    assert len(chunks) == 1
    assert chunks[0].end_seconds == 100


@pytest.mark.integration
def test_audio_chunking_with_real_file():
    """Test chunking with a real audio file.
    
    This test requires an MP3 file in tests/downloads/.
    To get the test file used in development:
    1. Use the YouTube downloader service, or 
    2. Place any MP3 file in tests/downloads/ directory
    
    The test will skip gracefully if no audio files are found.
    """
    downloads_dir = Path(__file__).parent.parent / "downloads"
    audio_files = list(downloads_dir.glob("*.mp3"))
    
    if not audio_files:
        pytest.skip("No MP3 files found in tests/downloads/ - add a file to run this test")
    
    test_file = audio_files[0]  # Use the first MP3 found
    
    # Test getting audio duration
    duration = get_audio_duration_seconds(str(test_file))
    assert duration > 0, f"Audio file {test_file.name} should have positive duration"
    
    # Test chunking a small portion (first 60 seconds to keep test fast)
    test_duration = min(60, duration)
    chunks = calculate_chunk_timestamps(
        total_duration_seconds=test_duration,
        chunk_duration=30,  # 30-second chunks for quick test
        overlap=5           # 5-second overlap
    )
    
    # Test creating actual chunks
    with tempfile.TemporaryDirectory() as temp_dir:
        chunk_files = []
        for i, chunk in enumerate(chunks[:2]):  # Only test first 2 chunks
            output_path = Path(temp_dir) / f"test_chunk_{i+1}.mp3"
            create_audio_chunk(str(test_file), str(output_path), chunk)
            
            assert output_path.exists(), f"Chunk file {output_path} was not created"
            assert output_path.stat().st_size > 0, f"Chunk file {output_path} is empty"
            chunk_files.append(output_path)
        
        print(f"✅ Successfully created {len(chunk_files)} chunks from {test_file.name}")
        print(f"   Original duration: {duration}s, Test duration: {test_duration}s")