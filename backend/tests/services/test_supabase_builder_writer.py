"""Test supabase_builder_writer.py database operations.

Tests: Basic CRUD operations for builder records
Used by: Development verification and CI pipeline
"""

import pytest
from backend_app.services.supabase_builder_writer import (
    create_builder_record,
    get_builder_by_slug,
    mark_builder_status
)


def test_create_and_retrieve_builder():
    """Test creating a builder record and retrieving it."""
    
    # Create test builder
    builder_id = create_builder_record(
        name="Test Builder",
        slug="test-builder-pytest",
        youtube_url="https://youtube.com/watch?v=test123"
    )
    
    assert builder_id is not None
    assert isinstance(builder_id, str)
    
    # Retrieve builder
    builder_profile = get_builder_by_slug("test-builder-pytest")
    
    assert builder_profile is not None
    assert builder_profile['builder']['name'] == "Test Builder"
    assert builder_profile['builder']['slug'] == "test-builder-pytest"
    assert builder_profile['builder']['status'] == "pending"


def test_update_builder_status():
    """Test updating builder status."""
    
    # Get existing test builder
    builder_profile = get_builder_by_slug("test-builder-pytest")
    assert builder_profile is not None
    
    builder_id = builder_profile['builder']['id']
    
    # Update status
    mark_builder_status(builder_id, "completed")
    
    # Verify update
    updated_profile = get_builder_by_slug("test-builder-pytest")
    assert updated_profile['builder']['status'] == "completed"