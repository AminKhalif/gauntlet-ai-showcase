"""Supabase storage service for file uploads."""

import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client() -> Client:
    """Get authenticated Supabase client.
    
    Returns:
        Authenticated Supabase client
        
    Raises:
        ValueError: If environment variables are missing
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment")
    
    return create_client(url, key)


def upload_audio_file(file_path: str, bucket_name: str = "audio-files") -> dict[str, str]:
    """Upload audio file to Supabase storage.
    
    Args:
        file_path: Local path to audio file
        bucket_name: Supabase storage bucket name
        
    Returns:
        Dict with 'public_url' and 'file_name' keys
        
    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If upload fails
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    client = get_supabase_client()
    original_name = Path(file_path).name
    
    # Clean filename for Supabase - replace invalid characters with underscores
    import re
    clean_name = re.sub(r'[^\w\-_\.]', '_', original_name)
    
    with open(file_path, 'rb') as file:
        response = client.storage.from_(bucket_name).upload(
            clean_name, 
            file.read()
        )
    
    if response.error:
        raise Exception(f"Upload failed: {response.error}")
    
    # Get public URL for private bucket (signed URL)
    signed_url = client.storage.from_(bucket_name).create_signed_url(
        clean_name, 
        expires_in=86400  # 24 hours
    )
    
    return {
        'public_url': signed_url['signedURL'],
        'file_name': clean_name
    }