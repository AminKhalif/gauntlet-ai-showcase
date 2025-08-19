# How to Run Tests - Backend Pipeline

Guide for running the audio transcription pipeline tests.

## Quick Start

1. **Install dependencies**:
   ```bash
   cd backend
   uv sync
   ```

2. **Set up environment**:
   ```bash
   # Add your Gemini API key to .env
   echo "GEMINI_API_KEY=your_key_here" >> .env
   ```

3. **Run tests**:
   ```bash
   # Run all tests
   uv run pytest

   # Test full transcript pipeline (requires Gemini API key + MP3 file)
   uv run pytest tests/services/test_full_transcript_orchestrator_integration.py -v -s
   ```

## Pipeline Overview

```
Audio MP3 → Audio Chunks → Gemini Transcription → Transcript Merger → Final Transcript
```

## Test Types

### Unit Tests (Fast)
Test individual functions with mocks:
```bash
uv run pytest tests/services/test_full_transcript_orchestrator.py
uv run pytest tests/services/test_audio_chunker.py
uv run pytest tests/services/test_gemini_diarization.py
```

### Integration Tests (Slower) 
Test complete workflows with real API calls:
```bash
# Full transcript pipeline (requires MP3 + Gemini API key)
uv run pytest tests/services/test_full_transcript_orchestrator_integration.py -v -s

# YouTube + GCS workflow (requires GCS credentials)  
uv run pytest tests/services/test_youtube_gcs_integration.py -v -s
```

## Test Files Required

Place test MP3 files in `backend/tests/downloads/`:
- Example: `AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3`

## Output Files

Tests save results to `backend/tests/downloads/`:
- **`final_transcript.txt`** - Complete merged transcript with timestamps
- **`chunks/transcript_chunk_001.txt`** - Individual chunk transcripts  
- **`chunks/audio_chunk_001.mp3`** - Individual audio chunks

## Environment Variables

```bash
# Required for integration tests
GEMINI_API_KEY=your_gemini_api_key_here

# Optional for GCS tests
GCP_PROJECT_ID=your_project_id
```

## Common Issues

- **ModuleNotFoundError**: Always use `uv run pytest` not bare `python`
- **Empty transcripts**: Check your Gemini API key is set correctly
- **FFmpeg errors**: Install FFmpeg (`brew install ffmpeg` on macOS)
- **No MP3 files**: Add test audio files to `tests/downloads/`