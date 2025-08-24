"""AssemblyAI API response models for speaker diarization.

Takes: AssemblyAI API JSON responses
Outputs: Typed dataclasses for transcription results with speaker labels
Used by: assemblyai_diarizer.py for type-safe transcript processing
"""

from dataclasses import dataclass
from typing import List, Optional, Literal


@dataclass(frozen=True)
class AssemblyAIUtterance:
    """Individual speaker utterance with timing and content."""
    speaker: str
    text: str
    start: int  # milliseconds
    end: int    # milliseconds
    confidence: float


@dataclass(frozen=True) 
class AssemblyAITranscript:
    """Complete AssemblyAI transcription result with speaker diarization."""
    id: str
    status: Literal["queued", "processing", "completed", "error"]
    text: Optional[str]
    utterances: List[AssemblyAIUtterance]
    audio_duration: Optional[int]  # milliseconds
    error: Optional[str]
    

@dataclass(frozen=True)
class SpeakerRole:
    """Mapping of AssemblyAI speaker labels to interview roles."""
    speaker_id: str
    role: Literal["Interviewer", "Interviewee"]
    first_appearance_time: int  # milliseconds


@dataclass(frozen=True)
class DiarizedTranscript:
    """Final processed transcript with speaker roles assigned."""
    utterances: List[AssemblyAIUtterance]
    speaker_roles: List[SpeakerRole] 
    total_duration_seconds: float
    speakers_detected: int