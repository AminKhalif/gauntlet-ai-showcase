"""Data models for Google Cloud Storage operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GCSUploadResult:
    """Result of uploading a file to Google Cloud Storage.
    
    Attributes:
        bucket_name: Name of the GCS bucket
        blob_name: Name of the uploaded blob/file
        public_url: Public URL to access the file
        size_bytes: Size of uploaded file in bytes
        content_type: MIME type of the uploaded file
    """
    bucket_name: str
    blob_name: str
    public_url: str
    size_bytes: int
    content_type: Optional[str] = None


@dataclass(frozen=True)
class GCSDownloadResult:
    """Result of downloading a file from Google Cloud Storage.
    
    Attributes:
        bucket_name: Name of the GCS bucket
        blob_name: Name of the downloaded blob/file
        local_path: Local file path where content was saved
        size_bytes: Size of downloaded file in bytes
        content_type: MIME type of the downloaded file
    """
    bucket_name: str
    blob_name: str
    local_path: str
    size_bytes: int
    content_type: Optional[str] = None


@dataclass(frozen=True)
class GCSFileInfo:
    """Information about a file in Google Cloud Storage.
    
    Attributes:
        bucket_name: Name of the GCS bucket
        blob_name: Name of the blob/file
        size_bytes: Size of file in bytes
        content_type: MIME type of the file
        created_at: ISO timestamp when file was created
        updated_at: ISO timestamp when file was last updated
    """
    bucket_name: str
    blob_name: str
    size_bytes: int
    content_type: Optional[str]
    created_at: str
    updated_at: str