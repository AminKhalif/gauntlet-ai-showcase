"""Integration tests for Google Cloud Storage service with real files."""

import os
import tempfile
from pathlib import Path
import pytest
from dotenv import load_dotenv

from backend_app.services.gcs_storage import upload_audio_file, download_audio_file, get_file_info, clean_blob_name_for_gcs
from backend_app.models.gcs_models import GCSUploadResult, GCSDownloadResult, GCSFileInfo

# Load environment variables
load_dotenv()


class TestGCSIntegration:
    """Test GCS service with real Google Cloud Storage and existing files."""
    
    @pytest.fixture
    def existing_podcast_path(self):
        """Path to existing podcast file in tests/downloads.
        
        This uses the real 1-hour podcast file that demonstrates our
        typical use case - large audio files that need to be stored
        in GCS for processing.
        """
        podcast_path = Path("tests/downloads/AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3")
        if not podcast_path.exists():
            pytest.skip(f"Podcast file not found: {podcast_path}")
        return str(podcast_path)
    
    @pytest.fixture
    def skip_if_no_gcs_config(self):
        """Skip test if GCS credentials not configured.
        
        Integration tests require real GCS credentials. This fixture
        gracefully skips tests if service-account.json is not set up, allowing
        unit tests to still run.
        """
        if not os.getenv("GCP_PROJECT_ID") or not Path("service-account.json").exists():
            pytest.skip("GCS credentials not configured. Set up service-account.json file first.")
    
    def test_upload_existing_podcast_file(self, existing_podcast_path, skip_if_no_gcs_config):
        """Test uploading the existing podcast file to GCS.
        
        This test verifies our ability to handle large files (1-hour podcasts ~50MB)
        which is essential for our use case. We need to ensure:
        1. Large file upload works without timeout
        2. File metadata is correctly captured  
        3. Public URL is generated for later access
        4. File size is preserved during upload
        
        This simulates the first step in our pipeline: storing the downloaded
        YouTube audio in GCS for chunking and processing.
        """
        # Get original file info
        original_size = Path(existing_podcast_path).stat().st_size
        blob_name = f"test_podcast_{Path(existing_podcast_path).name}"
        
        # Clean blob name for GCS compatibility
        clean_blob_name = clean_blob_name_for_gcs(blob_name)
        
        print(f"\n📁 Testing upload of: {existing_podcast_path}")
        print(f"📏 Original file size: {original_size:,} bytes")
        
        # Upload to GCS
        result = upload_audio_file(existing_podcast_path, blob_name=blob_name)
        
        # Verify upload result
        assert isinstance(result, GCSUploadResult)
        assert result.bucket_name == os.getenv("GCS_BUCKET_NAME")
        assert result.blob_name == clean_blob_name
        assert result.size_bytes == original_size
        assert "https://storage.googleapis.com" in result.public_url
        assert result.content_type is not None
        
        print(f"✅ Upload successful to: {result.public_url}")
        print(f"📦 Uploaded size: {result.size_bytes:,} bytes")
        
        # Cleanup test file from GCS
        self._cleanup_gcs_file(result.bucket_name, result.blob_name)
    
    def test_get_file_info_integration(self, existing_podcast_path, skip_if_no_gcs_config):
        """Test getting file metadata from GCS after upload.
        
        This test verifies we can retrieve file information from GCS,
        which is needed for:
        1. Tracking file processing status
        2. Validating file integrity before chunking
        3. Storing metadata in Supabase for the frontend
        4. Debugging upload issues
        """
        blob_name = f"info_test_{Path(existing_podcast_path).name}"
        
        # Clean blob name for GCS compatibility
        clean_blob_name = clean_blob_name_for_gcs(blob_name)
        
        # Upload file first
        upload_result = upload_audio_file(existing_podcast_path, blob_name=blob_name)
        
        try:
            # Get file info using the clean blob name
            file_info = get_file_info(clean_blob_name)
            
            # Verify file info matches upload
            assert isinstance(file_info, GCSFileInfo)
            assert file_info.bucket_name == upload_result.bucket_name
            assert file_info.blob_name == clean_blob_name
            assert file_info.size_bytes == upload_result.size_bytes
            assert file_info.created_at != ""
            assert file_info.updated_at != ""
            
            print(f"✅ File info retrieved successfully")
            print(f"📅 Created: {file_info.created_at}")
            print(f"📅 Updated: {file_info.updated_at}")
            
        finally:
            # Cleanup
            self._cleanup_gcs_file(upload_result.bucket_name, clean_blob_name)
    
    def test_upload_download_roundtrip(self, existing_podcast_path, skip_if_no_gcs_config):
        """Test uploading then downloading a file to verify integrity.
        
        This test simulates our complete workflow:
        1. YouTube downloader saves MP3 locally
        2. Upload MP3 to GCS for storage
        3. Later: Download MP3 from GCS for chunking  
        4. Process chunks with Gemini
        
        We need to verify the file stays intact through upload/download
        because any corruption would cause chunking or Gemini processing
        to fail mysteriously. This test catches data integrity issues early
        and ensures our 50MB+ podcast files can survive the roundtrip.
        """
        blob_name = f"roundtrip_test_{Path(existing_podcast_path).name}"
        original_size = Path(existing_podcast_path).stat().st_size
        
        # Clean blob name for GCS compatibility
        clean_blob_name = clean_blob_name_for_gcs(blob_name)
        
        print(f"\n🔄 Testing upload/download roundtrip")
        print(f"📁 Original: {existing_podcast_path}")
        print(f"📏 Size: {original_size:,} bytes")
        
        # Upload to GCS
        upload_result = upload_audio_file(existing_podcast_path, blob_name=blob_name)
        
        try:
            # Download to temporary location
            with tempfile.TemporaryDirectory() as temp_dir:
                download_path = os.path.join(temp_dir, "downloaded_podcast.mp3")
                download_result = download_audio_file(clean_blob_name, download_path)
                
                # Verify download result
                assert isinstance(download_result, GCSDownloadResult)
                assert download_result.bucket_name == upload_result.bucket_name
                assert download_result.blob_name == clean_blob_name
                assert download_result.local_path == download_path
                assert os.path.exists(download_path)
                
                # Verify file integrity (most important check)
                downloaded_size = Path(download_path).stat().st_size
                assert downloaded_size == original_size, f"Size mismatch: {downloaded_size} != {original_size}"
                
                print(f"✅ Download successful to: {download_path}")
                print(f"📏 Downloaded size: {downloaded_size:,} bytes")
                print(f"🔍 Integrity check: PASSED")
                
        finally:
            # Cleanup
            self._cleanup_gcs_file(upload_result.bucket_name, clean_blob_name)
    
    def _cleanup_gcs_file(self, bucket_name: str, blob_name: str):
        """Helper method to clean up test files from GCS.
        
        Removes uploaded test files to avoid cluttering the bucket
        and incurring unnecessary storage costs during development.
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
            print(f"🧹 Cleaned up test file: {blob_name}")
        except Exception as e:
            print(f"⚠️  Could not clean up test file {blob_name}: {e}")