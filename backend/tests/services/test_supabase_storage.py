#!/usr/bin/env python3
"""Test script for Supabase storage functionality."""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend_app.services.supabase_storage import upload_audio_file, get_supabase_client


def test_supabase_connection():
    """Test basic Supabase connection."""
    try:
        client = get_supabase_client()
        print("✅ Supabase connection successful")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


def test_upload_small_file():
    """Test uploading a small test file.
    
    Note: We create a small test file because the original 82MB MP3 
    exceeds Supabase's default upload limits. This tests the basic
    upload functionality before we implement chunking for large files.
    """
    # Create test file for this test
    test_file = Path("tests/downloads/test-small.mp3")
    test_file.write_text("test audio content for Supabase upload testing")
    
    try:
        print(f"📤 Uploading {test_file.name}...")
        result = upload_audio_file(str(test_file))
        print(f"✅ Upload successful!")
        print(f"   File name: {result['file_name']}")
        print(f"   URL: {result['public_url'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False
    finally:
        # Clean up test file
        test_file.unlink(missing_ok=True)


if __name__ == "__main__":
    print("🧪 Testing Supabase Storage...")
    print()
    
    # Test connection first
    if not test_supabase_connection():
        sys.exit(1)
    
    print()
    
    # Test file upload
    if not test_upload_small_file():
        sys.exit(1)
    
    print()
    print("🎉 All tests passed!")