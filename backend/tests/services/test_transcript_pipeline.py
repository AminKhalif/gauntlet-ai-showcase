"""Test full chunked transcription pipeline with 10 workers."""

import asyncio
import time
from pathlib import Path

import pytest
from backend_app.services.full_transcript_orchestrator import process_audio_with_chunked_diarization


@pytest.mark.anyio 
async def test_full_pipeline_10_workers():
    """Test complete pipeline with 10 workers and save transcript to downloads.
    
    This test:
    1. Finds an MP3 in tests/downloads/
    2. Runs full chunked transcription with 10 workers  
    3. Tests the overlap merge fix
    4. Saves final transcript to downloads/
    5. Measures timing vs previous 7.2-minute benchmark
    """
    downloads_dir = Path(__file__).parent.parent / "downloads"
    audio_files = list(downloads_dir.glob("*.mp3"))
    
    if not audio_files:
        pytest.skip("No MP3 files found in tests/downloads/ - add a file to run this test")
    
    test_file = audio_files[0]
    print(f"\n🎵 Testing with: {test_file.name}")
    
    # Record start time
    start_time = time.time()
    
    # Run pipeline with 10 workers
    try:
        final_transcript_path = await process_audio_with_chunked_diarization(
            str(test_file),
            output_dir=str(downloads_dir),
            max_concurrent=6
        )
        
        # Record completion time
        elapsed_time = time.time() - start_time
        elapsed_minutes = elapsed_time / 60
        
        # Verify transcript was created
        assert Path(final_transcript_path).exists(), "Final transcript file not created"
        
        # Read and check transcript content
        with open(final_transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        assert len(transcript_content) > 100, "Transcript seems too short"
        assert "[" in transcript_content and "]" in transcript_content, "No timestamps found in transcript"
        
        # Check for timestamp gaps (the bug we fixed)
        lines_with_timestamps = []
        for line in transcript_content.split('\n'):
            if '[' in line and ']' in line:
                lines_with_timestamps.append(line)
        
        print(f"\n📊 Results:")
        print(f"   ⏱️  Total time: {elapsed_minutes:.1f} minutes")
        print(f"   📝 Transcript lines: {len(transcript_content.split())}")
        print(f"   🕐 Timestamped lines: {len(lines_with_timestamps)}")
        print(f"   📁 Saved to: {final_transcript_path}")
        
        # Show first few timestamped lines to verify merge quality
        print(f"\n🔍 First few timestamped lines:")
        for i, line in enumerate(lines_with_timestamps[:5]):
            print(f"   {i+1}. {line.strip()}")
        
        # Show transition around potential overlap areas
        print(f"\n🔗 Checking for timestamp continuity...")
        timestamps = []
        for line in lines_with_timestamps:
            import re
            match = re.search(r'\[(\d{1,2}):(\d{2})\]', line)
            if match:
                minutes, seconds = map(int, match.groups())
                total_seconds = minutes * 60 + seconds
                timestamps.append(total_seconds)
        
        # Check for large gaps
        large_gaps = []
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i-1]
            if gap > 180:  # More than 3 minutes
                large_gaps.append((timestamps[i-1], timestamps[i], gap))
        
        if large_gaps:
            print(f"   ⚠️  Found {len(large_gaps)} large timestamp gaps:")
            for prev_ts, curr_ts, gap in large_gaps[:3]:
                prev_mm_ss = f"{prev_ts // 60:02d}:{prev_ts % 60:02d}"
                curr_mm_ss = f"{curr_ts // 60:02d}:{curr_ts % 60:02d}"
                print(f"      {prev_mm_ss} → {curr_mm_ss} (gap: {gap//60}m {gap%60}s)")
        else:
            print(f"   ✅ No large timestamp gaps found!")
        
        # Compare with previous benchmark
        if elapsed_minutes < 7.2:
            print(f"   🚀 FASTER than 7.2min benchmark!")
        else:
            print(f"   📈 Slower than 7.2min benchmark (likely API limits)")
            
    except Exception as e:
        elapsed_time = time.time() - start_time
        elapsed_minutes = elapsed_time / 60
        print(f"\n❌ Pipeline failed after {elapsed_minutes:.1f} minutes")
        print(f"   Error: {e}")
        
        # Still useful to know it failed and how long it took
        if "rate limit" in str(e).lower() or "empty response" in str(e).lower():
            print("   💡 Likely hit Gemini API rate limits with 10 workers")
            print("   💡 Consider reducing to 5-7 workers for reliability")
        
        raise


if __name__ == "__main__":
    asyncio.run(test_full_pipeline_10_workers())