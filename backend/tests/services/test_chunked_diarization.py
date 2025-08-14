"""Tests for chunked diarization service."""

import pytest
from unittest.mock import Mock, patch
from dataclasses import dataclass
from typing import List

from backend_app.services.chunked_diarization import (
    extract_timestamp_seconds,
    merge_chunk_transcripts,
    validate_timestamps_monotonic,
    validate_transcript_completeness,
    create_absolute_timestamp_prompt,
    ChunkTranscriptResult
)
from backend_app.models.audio_chunker_models import ChunkTimestamp


class TestExtractTimestampSeconds:
    """Test timestamp extraction from transcript lines."""
    
    def test_extract_valid_timestamp(self):
        """Test extracting valid [MM:SS] timestamp."""
        line = "Interviewer: [05:30] This is a question"
        result = extract_timestamp_seconds(line)
        assert result == 330  # 5*60 + 30
    
    def test_extract_zero_timestamp(self):
        """Test extracting [00:00] timestamp."""
        line = "Interviewee: [00:00] Starting response"
        result = extract_timestamp_seconds(line)
        assert result == 0
    
    def test_extract_large_timestamp(self):
        """Test extracting larger timestamp like [45:15]."""
        line = "Interviewer: [45:15] Another question"
        result = extract_timestamp_seconds(line)
        assert result == 2715  # 45*60 + 15
    
    def test_no_timestamp_returns_none(self):
        """Test line without timestamp returns None."""
        line = "This line has no timestamp"
        result = extract_timestamp_seconds(line)
        assert result is None
    
    def test_malformed_timestamp_returns_none(self):
        """Test malformed timestamp returns None."""
        line = "Bad timestamp [5:3] here"
        result = extract_timestamp_seconds(line)
        assert result is None


class TestMergeChunkTranscripts:
    """Test merging overlapping chunk transcripts."""
    
    def test_merge_two_chunks_with_overlap(self):
        """Test merging two chunks with overlapping timestamps."""
        chunk1 = ChunkTranscriptResult(
            chunk_number=1,
            start_seconds=0,
            end_seconds=480,
            transcript_text="Interviewer: [00:30] Question 1\nInterviewee: [01:00] Answer 1\nInterviewer: [07:30] Question 2",
            audio_file_path="chunk1.mp3",
            transcript_file_path="transcript1.txt"
        )
        
        chunk2 = ChunkTranscriptResult(
            chunk_number=2,
            start_seconds=450,
            end_seconds=930,
            transcript_text="Interviewer: [07:15] Overlap question\nInterviewer: [08:00] New question\nInterviewee: [08:30] New answer",
            audio_file_path="chunk2.mp3",
            transcript_file_path="transcript2.txt"
        )
        
        result = merge_chunk_transcripts([chunk1, chunk2], tolerance_seconds=2)
        lines = result.split('\n')
        
        # Should keep all lines from chunk 1
        assert "Interviewer: [00:30] Question 1" in lines
        assert "Interviewee: [01:00] Answer 1" in lines
        assert "Interviewer: [07:30] Question 2" in lines
        
        # Should drop overlapping line from chunk 2 (7:15 <= 8:00-2 = 6:00 is false, so keep it)
        # Actually 7:15 = 435s, cutoff = 480-2 = 478s, so 435 <= 478, so DROP it
        assert "Interviewer: [07:15] Overlap question" not in lines
        
        # Should keep non-overlapping lines from chunk 2
        assert "Interviewer: [08:00] New question" in lines
        assert "Interviewee: [08:30] New answer" in lines
    
    def test_merge_single_chunk(self):
        """Test merging single chunk returns original content."""
        chunk1 = ChunkTranscriptResult(
            chunk_number=1,
            start_seconds=0,
            end_seconds=480,
            transcript_text="Interviewer: [00:30] Only question\nInterviewee: [01:00] Only answer",
            audio_file_path="chunk1.mp3",
            transcript_file_path="transcript1.txt"
        )
        
        result = merge_chunk_transcripts([chunk1])
        assert result == "Interviewer: [00:30] Only question\nInterviewee: [01:00] Only answer"
    
    def test_merge_empty_chunks_raises_error(self):
        """Test merging empty chunk list raises ValueError."""
        with pytest.raises(ValueError, match="No chunk results to merge"):
            merge_chunk_transcripts([])
    
    def test_merge_chunks_out_of_order(self):
        """Test merging chunks in wrong order still works (gets sorted)."""
        chunk2 = ChunkTranscriptResult(
            chunk_number=2,
            start_seconds=450,
            end_seconds=930,
            transcript_text="Interviewer: [08:00] Second chunk",
            audio_file_path="chunk2.mp3",
            transcript_file_path="transcript2.txt"
        )
        
        chunk1 = ChunkTranscriptResult(
            chunk_number=1,
            start_seconds=0,
            end_seconds=480,
            transcript_text="Interviewer: [01:00] First chunk",
            audio_file_path="chunk1.mp3",
            transcript_file_path="transcript1.txt"
        )
        
        # Pass chunks in wrong order
        result = merge_chunk_transcripts([chunk2, chunk1])
        lines = result.split('\n')
        
        # Should still be in correct chronological order
        assert lines[0] == "Interviewer: [01:00] First chunk"
        assert lines[1] == "Interviewer: [08:00] Second chunk"


class TestValidateTimestampsMonotonic:
    """Test timestamp monotonicity validation."""
    
    def test_monotonic_timestamps_unchanged(self):
        """Test transcript with monotonic timestamps is unchanged."""
        transcript = "Interviewer: [01:00] First\nInterviewee: [02:00] Second\nInterviewer: [03:00] Third"
        result = validate_timestamps_monotonic(transcript)
        assert result == transcript
    
    def test_backwards_timestamp_removed(self):
        """Test line with backwards timestamp is removed."""
        transcript = "Interviewer: [03:00] Third\nInterviewee: [02:00] Second\nInterviewer: [04:00] Fourth"
        result = validate_timestamps_monotonic(transcript)
        lines = result.split('\n')
        
        assert "Interviewer: [03:00] Third" in lines
        assert "Interviewee: [02:00] Second" not in lines  # Should be removed
        assert "Interviewer: [04:00] Fourth" in lines
    
    def test_non_timestamped_lines_preserved(self):
        """Test lines without timestamps are preserved."""
        transcript = "No timestamp here\nInterviewer: [01:00] First\nAnother non-timestamped line\nInterviewer: [02:00] Second"
        result = validate_timestamps_monotonic(transcript)
        lines = result.split('\n')
        
        assert "No timestamp here" in lines
        assert "Another non-timestamped line" in lines
        assert len(lines) == 4


class TestValidateTranscriptCompleteness:
    """Test transcript completeness validation."""
    
    def test_complete_transcript(self):
        """Test transcript that covers expected duration."""
        transcript = "Interviewer: [01:00] Start\nInterviewee: [58:30] Near end\nInterviewer: [59:45] Final"
        expected_duration = 3600  # 60 minutes
        
        is_valid, message = validate_transcript_completeness(transcript, expected_duration, tolerance_seconds=30)
        
        assert is_valid is True
        assert "Complete" in message
        assert "3585s" in message  # 59:45 = 3585 seconds
    
    def test_incomplete_transcript(self):
        """Test transcript that doesn't cover expected duration."""
        transcript = "Interviewer: [01:00] Start\nInterviewee: [30:00] Middle\nInterviewer: [45:00] End too early"
        expected_duration = 3600  # 60 minutes
        
        is_valid, message = validate_transcript_completeness(transcript, expected_duration, tolerance_seconds=30)
        
        assert is_valid is False
        assert "Incomplete" in message
        assert "missing" in message
    
    def test_no_timestamps_in_transcript(self):
        """Test transcript with no timestamps fails validation."""
        transcript = "No timestamps in this transcript at all"
        expected_duration = 3600
        
        is_valid, message = validate_transcript_completeness(transcript, expected_duration)
        
        assert is_valid is False
        assert "No timestamps found" in message


class TestCreateAbsoluteTimestampPrompt:
    """Test absolute timestamp prompt creation."""
    
    def test_prompt_contains_chunk_timing(self):
        """Test prompt contains chunk start/end times."""
        chunk_timestamp = ChunkTimestamp(start_seconds=300, end_seconds=780, chunk_number=2)
        prompt = create_absolute_timestamp_prompt(chunk_timestamp)
        
        assert "seconds 300–780" in prompt
        assert "[05:00]" in prompt  # 300 seconds = 5:00
        assert "[13:00]" in prompt  # 780 seconds = 13:00
    
    def test_prompt_contains_role_instructions(self):
        """Test prompt contains speaker role instructions."""
        chunk_timestamp = ChunkTimestamp(start_seconds=0, end_seconds=480, chunk_number=1)
        prompt = create_absolute_timestamp_prompt(chunk_timestamp)
        
        assert "INTERVIEWER" in prompt
        assert "INTERVIEWEE" in prompt
        assert "ABSOLUTE time from the full episode" in prompt
        assert "not relative to this chunk" in prompt