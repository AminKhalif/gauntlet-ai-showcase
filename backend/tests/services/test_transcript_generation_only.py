"""Test transcript generation with real timestamps and full merging."""

import asyncio
import pytest
from pathlib import Path
from backend_app.services.gemini_chunk_transcriber import transcribe_audio_chunk
from backend_app.services.audio_chunk_planner import plan_audio_chunks
from backend_app.services.chunk_transcript_merger import process_transcript_merge
from backend_app.services.ffmpeg_audio_splitter import get_audio_duration_seconds

@pytest.mark.anyio
async def test_transcript_generation():
    """Test transcription with real timestamps and full merging pipeline."""
    
    downloads_dir = Path("tests/downloads")
    chunks_dir = downloads_dir / "chunks"
    audio_file = downloads_dir / "AI for Software Engineers： The Perfect Development Workflow (Palmer Wenzel of Gauntlet AI).mp3"
    
    if not audio_file.exists():
        pytest.skip(f"Audio file not found: {audio_file}")
    
    # Get REAL chunk timestamps using existing logic
    chunk_timestamps = plan_audio_chunks(str(audio_file))
    total_duration = get_audio_duration_seconds(str(audio_file))
    
    print(f"🎵 Audio duration: {total_duration}s ({total_duration//60}:{total_duration%60:02d})")
    print(f"📊 Planned {len(chunk_timestamps)} chunks")
    
    # Find existing chunk files
    chunk_files = sorted(list(chunks_dir.glob("audio_chunk_*.mp3")))
    if not chunk_files:
        pytest.skip("No chunk files found - run full pipeline test first")
    
    # Test transcription on ALL chunks CONCURRENTLY (like real pipeline)
    max_concurrent = 6
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single_chunk(i, chunk_timestamp, chunk_file):
        async with semaphore:
            start_mm_ss = f"{chunk_timestamp.start_seconds//60:02d}:{chunk_timestamp.start_seconds%60:02d}"
            end_mm_ss = f"{chunk_timestamp.end_seconds//60:02d}:{chunk_timestamp.end_seconds%60:02d}"
            
            print(f"\n🎵 Chunk {i+1}: {start_mm_ss} → {end_mm_ss}")
            print(f"📁 File: {chunk_file.name}")
            
            result = await transcribe_audio_chunk(chunk_timestamp, str(chunk_file))
            
            print(f"✅ Success! Length: {len(result.transcript_text)} chars")
            print(f"📝 First 150 chars: {result.transcript_text[:150]}...")
            
            # Save individual chunk transcript
            transcript_file = chunks_dir / f"transcript_chunk_{i+1:03d}.txt"
            with open(transcript_file, 'w') as f:
                f.write(result.transcript_text)
            
            return result
    
    # Process all chunks concurrently
    tasks = [
        process_single_chunk(i, chunk_timestamps[i], chunk_files[i])
        for i in range(min(len(chunk_timestamps), len(chunk_files)))
    ]
    
    try:
        transcript_results = await asyncio.gather(*tasks)
    except Exception as e:
        print(f"❌ Concurrent processing failed: {e}")
        return
    
    # Use existing merging logic to create final transcript
    if transcript_results:
        print(f"\n🔗 Merging {len(transcript_results)} transcripts...")
        try:
            final_transcript = process_transcript_merge(transcript_results, total_duration)
            
            # Save final merged transcript
            final_path = downloads_dir / "final_transcript_test.txt"
            with open(final_path, 'w') as f:
                f.write(final_transcript)
            
            print(f"✅ Final transcript saved: {final_path}")
            print(f"📏 Final length: {len(final_transcript)} chars")
            
            # Show first few lines to verify timestamps
            lines = final_transcript.split('\n')[:5]
            print(f"\n📝 First few lines:")
            for line in lines:
                if line.strip():
                    print(f"   {line}")
                    
        except Exception as e:
            print(f"❌ Merging failed: {e}")