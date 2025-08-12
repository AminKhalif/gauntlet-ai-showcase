"""Tests for YouTube audio download service."""

import os
import sys
sys.path.append('src')
from backend_app.services.youtube_downloader import download_audio


def test_download_audio():
    """Test downloading YouTube video as MP3."""
    url = "https://www.youtube.com/watch?v=1OUIx1EDqiU&t=3s"
    output_dir = "tests/downloads"
    
    result = download_audio(url, output_dir)
    
    assert 'filepath' in result
    assert 'title' in result
    assert result['filepath'].endswith('.mp3')
    assert os.path.exists(result['filepath'])