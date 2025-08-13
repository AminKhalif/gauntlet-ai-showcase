"""Google Cloud Storage service for file operations."""

import os
from pathlib import Path
from typing import Optional
from google.cloud import storage
from google.cloud.exceptions import NotFound, GoogleCloudError
from dotenv import load_dotenv

from backend_app.models.gcs_models import GCSUploadResult, GCSDownloadResult, GCSFileInfo

load_dotenv()


def clean_blob_name_for_gcs(blob_name: str) -> str:
    """Clean blob name for Google Cloud Storage compatibility.
    
    Replaces characters that are not compatible with GCS blob naming
    requirements with underscores.
    
    Args:
        blob_name: Original blob name that may contain special characters
        
    Returns:
        Clean blob name with only alphanumeric, dash, underscore, and dot characters
    """
    import re
    return re.sub(r'[^\w\-_\.]', '_', blob_name)


def get_gcs_client() -> storage.Client:
    """Get authenticated Google Cloud Storage client.
    
    Returns:
        Authenticated GCS client
        
    Raises:
        ValueError: If environment variables are missing or service account file not found
        GoogleCloudError: If authentication fails
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    service_account_path = "./service-account.json"
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set in environment")
    
    if not Path(service_account_path).exists():
        raise ValueError(f"Service account file not found: {service_account_path}")
    
    try:
        return storage.Client.from_service_account_json(service_account_path, project=project_id)
    except Exception as e:
        raise GoogleCloudError(f"Failed to create GCS client: {e}")


def upload_audio_file(
    file_path: str, 
    blob_name: Optional[str] = None,
    bucket_name: Optional[str] = None
) -> GCSUploadResult:
    """Upload audio file to Google Cloud Storage.
    
    Args:
        file_path: Local path to audio file
        blob_name: Name for the blob in GCS (defaults to filename)
        bucket_name: GCS bucket name (defaults to GCS_BUCKET_NAME env var)
        
    Returns:
        GCSUploadResult with upload details
        
    Raises:
        FileNotFoundError: If local file doesn't exist
        ValueError: If bucket_name not provided and not in environment
        GoogleCloudError: If upload fails
    """
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not bucket_name:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("bucket_name parameter or GCS_BUCKET_NAME environment variable required")
    
    if not blob_name:
        blob_name = file_path_obj.name
    
    # Clean blob name for GCS compatibility
    clean_blob_name = clean_blob_name_for_gcs(blob_name)
    
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(clean_blob_name)
    
    try:
        # Upload file with metadata
        blob.upload_from_filename(file_path)
        
        # Get file size and content type
        file_size = file_path_obj.stat().st_size
        content_type = blob.content_type or "audio/mpeg"
        
        # Generate public URL
        public_url = f"https://storage.googleapis.com/{bucket_name}/{clean_blob_name}"
        
        return GCSUploadResult(
            bucket_name=bucket_name,
            blob_name=clean_blob_name,
            public_url=public_url,
            size_bytes=file_size,
            content_type=content_type
        )
        
    except Exception as e:
        raise GoogleCloudError(f"Upload failed for {clean_blob_name}: {e}")


def download_audio_file(
    blob_name: str,
    local_path: str,
    bucket_name: Optional[str] = None
) -> GCSDownloadResult:
    """Download audio file from Google Cloud Storage.
    
    Args:
        blob_name: Name of the blob in GCS
        local_path: Local path to save downloaded file
        bucket_name: GCS bucket name (defaults to GCS_BUCKET_NAME env var)
        
    Returns:
        GCSDownloadResult with download details
        
    Raises:
        ValueError: If bucket_name not provided and not in environment
        NotFound: If blob doesn't exist in bucket
        GoogleCloudError: If download fails
    """
    if not bucket_name:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("bucket_name parameter or GCS_BUCKET_NAME environment variable required")
    
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    try:
        # Check if blob exists
        if not blob.exists():
            raise NotFound(f"Blob {blob_name} not found in bucket {bucket_name}")
        
        # Create directory if it doesn't exist
        local_path_obj = Path(local_path)
        local_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        blob.download_to_filename(local_path)
        
        # Get file info
        blob.reload()  # Refresh blob metadata
        file_size = local_path_obj.stat().st_size
        
        return GCSDownloadResult(
            bucket_name=bucket_name,
            blob_name=blob_name,
            local_path=local_path,
            size_bytes=file_size,
            content_type=blob.content_type
        )
        
    except NotFound:
        raise
    except Exception as e:
        raise GoogleCloudError(f"Download failed for {blob_name}: {e}")


def get_file_info(blob_name: str, bucket_name: Optional[str] = None) -> GCSFileInfo:
    """Get information about a file in Google Cloud Storage.
    
    Args:
        blob_name: Name of the blob in GCS
        bucket_name: GCS bucket name (defaults to GCS_BUCKET_NAME env var)
        
    Returns:
        GCSFileInfo with file details
        
    Raises:
        ValueError: If bucket_name not provided and not in environment
        NotFound: If blob doesn't exist in bucket
        GoogleCloudError: If operation fails
    """
    if not bucket_name:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("bucket_name parameter or GCS_BUCKET_NAME environment variable required")
    
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    try:
        # Check if blob exists and get metadata
        blob.reload()
        
        return GCSFileInfo(
            bucket_name=bucket_name,
            blob_name=blob_name,
            size_bytes=blob.size or 0,
            content_type=blob.content_type,
            created_at=blob.time_created.isoformat() if blob.time_created else "",
            updated_at=blob.updated.isoformat() if blob.updated else ""
        )
        
    except NotFound:
        raise NotFound(f"Blob {blob_name} not found in bucket {bucket_name}")
    except Exception as e:
        raise GoogleCloudError(f"Failed to get info for {blob_name}: {e}")