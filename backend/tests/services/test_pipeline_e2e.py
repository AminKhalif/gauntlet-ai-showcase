"""End-to-end pipeline tests showing full YouTube to GCS workflow."""

import os
import tempfile
from pathlib import Path
import pytest
from dotenv import load_dotenv

from backend_app.services.youtube_downloader import download_youtube_audio
from backend_app.services.gcs_storage import upload_audio_file, download_audio_file
from backend_app.models.gcs_models import GCSUploadResult, GCSDownloadResult

# Load environment variables
load_dotenv()


class TestYouTubeToGCSPipeline:
    """Test the complete pipeline from YouTube URL to GCS storage.
    
    These tests demonstrate the full workflow that users will experience:
    1. Provide YouTube URL
    2. Download audio as MP3  
    3. Upload MP3 to GCS for storage
    4. Verify file is accessible for later chunking
    
    These are slower tests that require network access and should be run
    less frequently than unit tests, but they provide confidence that the
    entire system works together.
    """
    
    @pytest.fixture
    def skip_if_no_gcs_config(self):
        """Skip test if GCS credentials not configured.
        
        End-to-end tests require both YouTube access and GCS credentials.
        This fixture gracefully skips if environment isn't fully set up.
        """
        if not os.getenv("GCP_PROJECT_ID") or not Path("service-account.json").exists():
            pytest.skip("GCS credentials not configured. Set up service-account.json file first.")
    
    @pytest.fixture 
    def test_youtube_url(self):
        """Short YouTube video URL for testing.
        
        Uses a short video to minimize test time and bandwidth usage.
        In production, users will provide 1-hour podcast URLs, but for
        testing we use something quick and reliable.
        """
        # Short test video (replace with a reliable short video URL)
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (3:32)
    
    def test_youtube_to_gcs_complete_workflow(self, test_youtube_url, skip_if_no_gcs_config):
        """Test the complete workflow from YouTube URL to GCS storage.
        
        This test demonstrates the full user journey:
        1. User provides YouTube podcast URL
        2. System downloads audio as MP3
        3. System uploads MP3 to GCS for storage
        4. System can retrieve file for chunking/processing
        
        This test validates:
        - YouTube downloader works with real URLs
        - Downloaded files are valid MP3s
        - GCS upload handles real downloaded files
        - File sizes are preserved throughout pipeline
        - Integration between services works correctly
        
        Why this matters: This is exactly what happens when a user
        submits a podcast URL in the frontend. Any failure here
        would break the entire user experience.
        """
        print(f"\n🎬 Testing complete YouTube → GCS pipeline")
        print(f"🔗 YouTube URL: {test_youtube_url}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Step 1: Download from YouTube
            print(f"\n1️⃣ Downloading from YouTube...")
            download_path = download_youtube_audio(test_youtube_url, temp_dir)
            
            # Verify download worked
            assert os.path.exists(download_path), "YouTube download failed"
            download_size = Path(download_path).stat().st_size
            assert download_size > 0, "Downloaded file is empty"
            assert download_path.endswith('.mp3'), "Downloaded file is not MP3"
            
            print(f"✅ Downloaded: {Path(download_path).name}")
            print(f"📏 Size: {download_size:,} bytes")
            
            # Step 2: Upload to GCS
            print(f"\n2️⃣ Uploading to GCS...")
            blob_name = f"pipeline_test_{Path(download_path).name}"
            upload_result = upload_audio_file(download_path, blob_name=blob_name)
            
            # Verify upload worked
            assert isinstance(upload_result, GCSUploadResult)
            assert upload_result.size_bytes == download_size
            assert upload_result.blob_name == blob_name
            assert "https://storage.googleapis.com" in upload_result.public_url
            
            print(f"✅ Uploaded: {upload_result.blob_name}")
            print(f"🌐 URL: {upload_result.public_url}")
            print(f"📦 GCS Size: {upload_result.size_bytes:,} bytes")
            
            try:
                # Step 3: Verify we can download back from GCS
                print(f"\n3️⃣ Verifying GCS download...")
                gcs_download_path = os.path.join(temp_dir, "from_gcs.mp3")
                download_result = download_audio_file(blob_name, gcs_download_path)
                
                # Verify roundtrip integrity
                assert isinstance(download_result, GCSDownloadResult)
                assert os.path.exists(gcs_download_path)
                
                final_size = Path(gcs_download_path).stat().st_size
                assert final_size == download_size, f"Size changed: {final_size} != {download_size}"
                
                print(f"✅ Downloaded from GCS: {final_size:,} bytes")
                print(f"🔍 Integrity: PASSED (all sizes match)")
                
                # Step 4: Summary
                print(f"\n🎉 Complete pipeline test PASSED!")
                print(f"   YouTube → Local: {download_size:,} bytes")
                print(f"   Local → GCS: {upload_result.size_bytes:,} bytes") 
                print(f"   GCS → Local: {final_size:,} bytes")
                print(f"   Ready for chunking and Gemini processing!")
                
            finally:
                # Cleanup GCS file
                self._cleanup_gcs_file(upload_result.bucket_name, blob_name)
    
    def test_youtube_to_gcs_with_existing_podcast(self, skip_if_no_gcs_config):
        """Test uploading an existing downloaded podcast to demonstrate scalability.
        
        This test shows how the system handles realistic podcast files:
        1. Uses the existing 1-hour podcast from tests/downloads
        2. Uploads it to GCS (simulating the YouTube → GCS flow)
        3. Verifies large file handling works correctly
        
        This is faster than downloading from YouTube but tests the same
        GCS upload/download logic with production-sized files.
        
        Why this matters: Real podcasts are 50MB+ and 1+ hours long.
        We need to ensure our system can handle these without timeouts
        or memory issues.
        """
        # Check if existing podcast file is available
        podcast_path = Path("tests/downloads/AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3")
        if not podcast_path.exists():
            pytest.skip(f"Existing podcast not found: {podcast_path}")
        
        original_size = podcast_path.stat().st_size
        blob_name = f"pipeline_existing_{podcast_path.name}"
        
        print(f"\n📻 Testing with existing podcast file")
        print(f"📁 File: {podcast_path.name}")
        print(f"📏 Size: {original_size:,} bytes")
        
        # Upload existing podcast to GCS  
        print(f"\n⬆️  Uploading to GCS...")
        upload_result = upload_audio_file(str(podcast_path), blob_name=blob_name)
        
        # Verify upload of large file
        assert isinstance(upload_result, GCSUploadResult)
        assert upload_result.size_bytes == original_size
        assert upload_result.blob_name == blob_name
        
        print(f"✅ Large file upload successful!")
        print(f"📦 Uploaded: {upload_result.size_bytes:,} bytes")
        print(f"🌐 Available at: {upload_result.public_url}")
        print(f"🚀 Ready for chunking into 8-10 minute segments!")
        
        # Cleanup
        self._cleanup_gcs_file(upload_result.bucket_name, blob_name)
    
    def _cleanup_gcs_file(self, bucket_name: str, blob_name: str):
        """Helper method to clean up test files from GCS.
        
        Removes uploaded test files to avoid cluttering the bucket
        and incurring unnecessary storage costs during testing.
        """
        try:
            from google.cloud import storage
            client = storage.Client.from_service_account_json(
                "./service-account.json",
                project=os.getenv("GCP_PROJECT_ID")
            )
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            print(f"🧹 Cleaned up pipeline test file: {blob_name}")
        except Exception as e:
            print(f"⚠️  Could not clean up test file {blob_name}: {e}")