"""AssemblyAI speaker diarization for interview transcripts.

Takes: Audio files (.mp3) with 2 speakers (Interviewer/Interviewee)
Outputs: Formatted transcript string with speaker roles and timestamps  
Used by: Alternative to gemini_chunk_transcriber.py when Gemini diarization fails
"""

import os
from pathlib import Path
from typing import Dict, List

import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()


def transcribe_with_diarization(audio_file_path: str) -> str:
    """
    Transcribe audio file with AssemblyAI speaker diarization.
    
    Args:
        audio_file_path: Path to MP3 audio file
        
    Returns:
        Formatted transcript string with speaker labels and timestamps
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If API key missing or transcription fails
    """
    _configure_assemblyai()
    
    if not Path(audio_file_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2
    )
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config=config)
    
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f"AssemblyAI transcription failed: {transcript.error}")
    
    return _format_transcript_output(transcript)


def save_transcript_to_file(transcript_text: str, output_path: str) -> None:
    """
    Save transcript to text file.
    
    Args:
        transcript_text: Formatted transcript string
        output_path: Path where to save the transcript
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)


def _configure_assemblyai() -> None:
    """Configure AssemblyAI with API key from environment."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    aai.settings.api_key = api_key


def _format_transcript_output(transcript) -> str:
    """Format AssemblyAI transcript to match project output format."""
    utterances = transcript.utterances or []
    
    if not utterances:
        return "No utterances found in transcript."
    
    role_mapping = _assign_speaker_roles(utterances)
    
    lines = []
    lines.append("TRANSCRIPT WITH SPEAKER DIARIZATION")
    lines.append("=" * 80)
    lines.append("")
    
    for utterance in utterances:
        speaker = utterance.speaker
        role = role_mapping.get(speaker, f"Speaker_{speaker}")
        
        # Convert milliseconds to MM:SS format
        start_time = utterance.start / 1000.0
        end_time = utterance.end / 1000.0
        start_min, start_sec = int(start_time // 60), int(start_time % 60)
        end_min, end_sec = int(end_time // 60), int(end_time % 60)
        
        timestamp = f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}]"
        
        lines.append(f"{timestamp} {role} ({speaker}):")
        lines.append(f"  {utterance.text}")
        lines.append("")
    
    lines.append("=" * 80)
    duration_seconds = (transcript.audio_duration or 0) / 1000.0
    lines.append(f"Total duration: {duration_seconds:.1f} seconds")
    lines.append(f"Number of speakers detected: {len(role_mapping)}")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def _assign_speaker_roles(utterances) -> Dict[str, str]:
    """Assign Interviewer/Interviewee roles based on speaking order."""
    if not utterances:
        return {}
    
    # Find first appearance time for each speaker
    speaker_first_appearance = {}
    for utterance in utterances:
        speaker = utterance.speaker
        if speaker not in speaker_first_appearance:
            speaker_first_appearance[speaker] = utterance.start
    
    # Sort speakers by first appearance time
    speakers_by_time = sorted(speaker_first_appearance.items(), key=lambda x: x[1])
    
    # Assign roles: first speaker = Interviewer, rest = Interviewee
    role_mapping = {}
    for i, (speaker, _) in enumerate(speakers_by_time):
        if i == 0:
            role_mapping[speaker] = "Interviewer"
        else:
            role_mapping[speaker] = "Interviewee"
    
    return role_mapping