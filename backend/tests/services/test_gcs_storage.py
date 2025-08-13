"""Unit tests for Google Cloud Storage service."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

from backend_app.services.gcs_storage import (
    get_gcs_client,
    upload_audio_file,
    download_audio_file,
    get_file_info
)
from backend_app.models.gcs_models import GCSUploadResult, GCSDownloadResult, GCSFileInfo


class TestGetGcsClient:
    """Test GCS client creation."""
    
    @patch.dict(os.environ, {
        "GCP_PROJECT_ID": "test-project",
        "GCP_SERVICE_ACCOUNT_JSON": '{"type": "service_account", "project_id": "test-project"}'
    })
    @patch("backend_app.services.gcs_storage.storage.Client.from_service_account_info")
    def test_get_gcs_client_success(self, mock_client):
        """Test successful GCS client creation."""
        mock_client.return_value = Mock()
        
        client = get_gcs_client()
        
        assert client is not None
        mock_client.assert_called_once()
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_gcs_client_missing_project_id(self):
        """Test GCS client creation fails without project ID."""
        with pytest.raises(ValueError, match="GCP_PROJECT_ID must be set"):
            get_gcs_client()
    
    @patch.dict(os.environ, {"GCP_PROJECT_ID": "test-project"})
    def test_get_gcs_client_missing_json(self):
        """Test GCS client creation fails without service account JSON."""
        with pytest.raises(ValueError, match="GCP_SERVICE_ACCOUNT_JSON must be set"):
            get_gcs_client()
    
    @patch.dict(os.environ, {
        "GCP_PROJECT_ID": "test-project",
        "GCP_SERVICE_ACCOUNT_JSON": "invalid-json"
    })
    def test_get_gcs_client_invalid_json(self):
        """Test GCS client creation fails with invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            get_gcs_client()


class TestUploadAudioFile:
    """Test audio file upload functionality."""
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_upload_audio_file_success(self, mock_get_client):
        """Test successful audio file upload."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(b"fake audio data")
            temp_file_path = temp_file.name
        
        try:
            # Mock GCS client and bucket
            mock_client = Mock()
            mock_bucket = Mock()
            mock_blob = Mock()
            
            mock_get_client.return_value = mock_client
            mock_client.bucket.return_value = mock_bucket
            mock_bucket.blob.return_value = mock_blob
            mock_blob.content_type = "audio/mpeg"
            
            # Test upload
            result = upload_audio_file(temp_file_path)
            
            # Assertions
            assert isinstance(result, GCSUploadResult)
            assert result.bucket_name == "test-bucket"
            assert result.blob_name == Path(temp_file_path).name
            assert result.size_bytes > 0
            assert result.content_type == "audio/mpeg"
            assert "https://storage.googleapis.com" in result.public_url
            
            # Verify GCS calls
            mock_blob.upload_from_filename.assert_called_once_with(temp_file_path)
            
        finally:
            # Cleanup
            os.unlink(temp_file_path)
    
    def test_upload_audio_file_not_found(self):
        """Test upload fails when file doesn't exist."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            upload_audio_file("/nonexistent/file.mp3")
    
    @patch.dict(os.environ, {}, clear=True)
    def test_upload_audio_file_no_bucket(self):
        """Test upload fails when bucket name not provided."""
        with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
            with pytest.raises(ValueError, match="bucket_name parameter or GCS_BUCKET_NAME"):
                upload_audio_file(temp_file.name)
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    def test_upload_audio_file_custom_blob_name(self, mock_get_client):
        """Test upload with custom blob name."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(b"fake audio data")
            temp_file_path = temp_file.name
        
        try:
            # Mock GCS client
            mock_client = Mock()
            mock_bucket = Mock()
            mock_blob = Mock()
            
            mock_get_client.return_value = mock_client
            mock_client.bucket.return_value = mock_bucket
            mock_bucket.blob.return_value = mock_blob
            mock_blob.content_type = "audio/mpeg"
            
            # Test upload with custom name
            result = upload_audio_file(temp_file_path, blob_name="custom-name.mp3", bucket_name="test-bucket")
            
            assert result.blob_name == "custom-name.mp3"
            mock_bucket.blob.assert_called_with("custom-name.mp3")
            
        finally:
            os.unlink(temp_file_path)


class TestDownloadAudioFile:
    """Test audio file download functionality."""
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_download_audio_file_success(self, mock_get_client):
        """Test successful audio file download."""
        # Mock GCS client and blob
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()
        
        mock_get_client.return_value = mock_client
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.exists.return_value = True
        mock_blob.content_type = "audio/mpeg"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = os.path.join(temp_dir, "downloaded.mp3")
            
            # Create fake downloaded file (simulates download_to_filename)
            def fake_download(path):
                with open(path, "wb") as f:
                    f.write(b"fake downloaded audio")
            
            mock_blob.download_to_filename.side_effect = fake_download
            
            # Test download
            result = download_audio_file("test-blob.mp3", local_path)
            
            # Assertions
            assert isinstance(result, GCSDownloadResult)
            assert result.bucket_name == "test-bucket"
            assert result.blob_name == "test-blob.mp3"
            assert result.local_path == local_path
            assert result.size_bytes > 0
            assert result.content_type == "audio/mpeg"
            
            # Verify file was created
            assert os.path.exists(local_path)
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_download_audio_file_not_found(self, mock_get_client):
        """Test download fails when blob doesn't exist."""
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()
        
        mock_get_client.return_value = mock_client
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.exists.return_value = False
        
        from google.cloud.exceptions import NotFound
        with pytest.raises(NotFound, match="not found in bucket"):
            download_audio_file("nonexistent.mp3", "/tmp/test.mp3")


class TestGetFileInfo:
    """Test file info retrieval functionality."""
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_get_file_info_success(self, mock_get_client):
        """Test successful file info retrieval."""
        from datetime import datetime
        
        # Mock GCS client and blob
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()
        
        mock_get_client.return_value = mock_client
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        # Mock blob metadata
        mock_blob.size = 1024
        mock_blob.content_type = "audio/mpeg"
        mock_blob.time_created = datetime(2024, 1, 1, 12, 0, 0)
        mock_blob.updated = datetime(2024, 1, 1, 12, 30, 0)
        
        # Test get info
        result = get_file_info("test-file.mp3")
        
        # Assertions
        assert isinstance(result, GCSFileInfo)
        assert result.bucket_name == "test-bucket"
        assert result.blob_name == "test-file.mp3"
        assert result.size_bytes == 1024
        assert result.content_type == "audio/mpeg"
        assert "2024-01-01T12:00:00" in result.created_at
        assert "2024-01-01T12:30:00" in result.updated_at
        
        # Verify blob reload was called
        mock_blob.reload.assert_called_once()
    
    @patch("backend_app.services.gcs_storage.get_gcs_client")
    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_get_file_info_not_found(self, mock_get_client):
        """Test get info fails when blob doesn't exist."""
        mock_client = Mock()
        mock_bucket = Mock()
        mock_blob = Mock()
        
        mock_get_client.return_value = mock_client
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        from google.cloud.exceptions import NotFound
        mock_blob.reload.side_effect = NotFound("Blob not found")
        
        with pytest.raises(NotFound, match="not found in bucket"):
            get_file_info("nonexistent.mp3")