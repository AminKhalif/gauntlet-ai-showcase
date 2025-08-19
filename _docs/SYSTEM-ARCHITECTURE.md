# System Architecture

## Current Implementation Status

### Backend (Python 3.12) - **In Progress**
Core audio processing pipeline is functional. FastAPI server not yet implemented.

**Completed Components:**
- ✅ **Audio Processing**: YouTube MP3 download and chunking
- ✅ **Transcription**: Gemini-powered speech-to-text with timestamps
- ✅ **Diarization**: Speaker identification and segmentation  
- ✅ **Transcript Merging**: Overlap handling and validation
- 🚧 **LangExtract Integration**: Currently implementing workflow extraction

**Pipeline Flow:**
```
YouTube URL → MP3 Download → Audio Chunking → Gemini Transcription → 
Speaker Diarization → Transcript Merging → [NEW] LangExtract → Workflow Cards
```

**Tech Stack:**
- **uv** - Package management and dependency resolution
- **Google Gemini 2.5 Pro** - Audio transcription and diarization
- **LangExtract** - Structured workflow extraction from transcripts
- **FFmpeg** - Audio processing and chunking
- **pytest** - Testing framework
- **dataclasses** - Type-safe data models

### Frontend (Next.js/React) - **In Progress** 
UI framework established, workflow display components under development.

**Tech Stack:**
- **Next.js** - React framework with TypeScript
- **React** - Component-based UI
- **TypeScript** - Type safety and developer experience

### Data Flow

**Input:** YouTube podcast URLs featuring AI builders discussing workflows

**Processing:**
1. **Audio Extraction** - Download and chunk MP3 for parallel processing
2. **Transcription** - Generate timestamped text with speaker identification
3. **Workflow Extraction** - Use LangExtract to identify and structure workflow patterns
4. **Card Generation** - Map extractions to 6 standardized workflow cards

**Output:** Structured workflow profiles with timestamps for interactive playback

## Current Work: LangExtract Integration

**Goal:** Extract structured workflow cards from raw interview transcripts

**Implementation:**
- **Schema Design** - Define extraction classes for 6 workflow cards
- **Few-Shot Training** - Build domain-specific examples from real transcripts  
- **Timestamp Mapping** - Correlate extracted text back to audio timestamps
- **Validation** - Interactive HTML visualization for quality review

**Workflow Cards Being Extracted:**
1. Planning & Scoping
2. Context Management  
3. Codegen Loop
4. Verification & Safeguards
5. Iteration Style
6. Deployment & Delivery

## Planned Components

### FastAPI Server
RESTful API for frontend to access processed workflow data
- Workflow profile endpoints
- Audio playback coordination
- Real-time processing status

### Database Layer  
Persistent storage for processed workflows and metadata
- Workflow profiles and cards
- Audio file metadata
- User interactions and feedback

### Interactive Frontend
Rich UI for comparing and exploring workflow patterns
- Side-by-side workflow comparison
- Audio playback with synchronized workflow highlighting
- Search and filtering across workflow patterns

## Architecture Principles

**Modularity** - Each processing stage is independent and testable
**Type Safety** - Comprehensive type hints and dataclass models
**Scalability** - Async processing with parallel audio chunk handling
**Observability** - Structured logging and processing artifacts for debugging