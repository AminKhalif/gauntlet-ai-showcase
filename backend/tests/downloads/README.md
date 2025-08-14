# Downloads Folder

This folder contains test audio files used for testing our audio processing pipeline.

## Purpose

- **Test Data Storage**: Contains audio files downloaded for testing purposes
- **Integration Testing**: Provides real-world audio data for end-to-end pipeline testing
- **Development**: Allows testing of chunking, diarization, and transcription services

## Current Test Files

### AI for Software Engineers Podcast
- **File**: `AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3`
- **Source**: Downloaded using our YouTube downloader service (`src/backend_app/services/youtube_downloader.py`)
- **Original URL**: YouTube podcast episode about AI workflows for developers
- **Duration**: ~1 hour
- **Purpose**: Testing Gemini diarization and audio processing pipeline

## For Developers Cloning This Repo

⚠️ **Note**: The actual podcast MP3 file is **not included** in this repository due to size and copyright considerations.

To run tests that require this audio file:

1. **Option 1**: Use our YouTube downloader to download the same podcast
   ```bash
   # Example usage of youtube_downloader.py
   uv run python -m backend_app.services.youtube_downloader
   ```

2. **Option 2**: Replace with your own test audio file
   - Add any ~1 hour audio file to this folder
   - Update test file paths accordingly
   - Ensure the audio contains clear speaker separation for diarization testing

3. **Option 3**: Skip audio-dependent tests
   - Tests will gracefully handle missing audio files
   - Focus on other service components that don't require large audio files

## File Structure

```
downloads/
├── README.md                          # This file
├── *.mp3                             # Audio test files (not in git)
├── *.txt                             # Generated transcripts and outputs
└── diarized_transcript.txt           # Output from Gemini diarization tests
```

## Testing Guidelines

- Audio files in this folder are for testing purposes only
- Generated outputs (transcripts, etc.) are saved here alongside source files
- Keep test files organized and document their purpose
- Large audio files should not be committed to the repository