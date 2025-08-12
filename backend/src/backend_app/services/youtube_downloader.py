"""YouTube audio download service."""

import os
from pathlib import Path
import yt_dlp


def download_audio(url: str, output_dir: str) -> dict[str, str]:
    """Download audio from YouTube video as MP3.
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save the MP3 file
        
    Returns:
        Dict with 'filepath' and 'title' keys
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'nocheckcertificate': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        ydl.download([url])
        
        filepath = f"{output_dir}/{title}.mp3"
        
        return {
            'filepath': filepath,
            'title': title
        }