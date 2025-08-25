# Current Task: LangExtract Integration

## Goal
Integrate Google's LangExtract library to extract structured workflow cards from AI builder interview transcripts.

## Status: In Progress (Today's Work)

### ✅ Completed
- [x] Added LangExtract dependency via `uv add langextract`
- [x] Updated project documentation (README, project-overview, system-architecture)
- [x] Defined 6 workflow cards structure (replacing previous 7-category approach)

### 🚧 Currently Working On
- [ ] **Data Models**: Create workflow_models.py with 6-card structure
- [ ] **Transcript Analysis**: Extract few-shot examples from real transcript content  
- [ ] **Service Implementation**: Build LangExtract service with timestamp mapping
- [ ] **Integration**: Connect to existing transcript pipeline

### 📋 Remaining Tasks
- [ ] **Few-Shot Examples**: Build domain-specific examples from transcript
- [ ] **Timestamp Correlation**: Map LangExtract char positions to audio timestamps
- [ ] **Testing**: Validate extraction on sample transcript
- [ ] **Artifacts**: Generate JSONL + HTML visualization for review

## Workflow Cards Being Extracted

1. **Planning & Scoping** - Goals, constraints, definition of done
2. **Context Management** - How they prep and feed info to models  
3. **Codegen Loop** - How they steer the model to write code
4. **Verification & Safeguards** - How they check output before it lands
5. **Iteration Style** - How they evolve solutions over time
6. **Deployment & Delivery** - How changes reach users

## Technical Implementation

### Data Flow
```
Raw Transcript → LangExtract Processing → Workflow Entities → 6 Workflow Cards
```

### Key Components
- **WorkflowEntity**: Single extracted element with timestamp correlation
- **WorkflowProfile**: Complete 6-card profile for one AI builder
- **TranscriptSegment**: Parsed transcript with timing for mapping
- **ExtractionResult**: Full result with artifacts and metadata

### LangExtract Configuration
```python
{
    "model_id": "gemini-2.5-flash",    # Speed/cost/quality balance
    "extraction_passes": 3,             # Better recall
    "max_workers": 20,                  # Parallel processing
    "max_char_buffer": 1000            # Optimal chunk size
}
```

## Integration Points

### Existing Pipeline
`YouTube → MP3 → Transcription → Diarization → Transcript Merging`

### Enhanced Pipeline  
`YouTube → MP3 → Transcription → Diarization → Transcript Merging → **LangExtract** → Workflow Cards`

### Critical Technical Challenge
**Timestamp Mapping**: LangExtract returns character positions - need to map these back to audio timestamps for UI correlation.

## Source Files
- **Transcript Sample**: `backend/tests/downloads/assembyly_ai_transcript.txt`
- **Existing Services**: `transcript_service.py`, `transcript_merger.py`
- **New Models**: `workflow_models.py` (in progress)
- **New Service**: `langextract_service.py` (planned)

## Success Criteria
- Extract 85-95% of relevant workflow elements
- Maintain ±2 second timestamp accuracy
- Process transcripts in <5 minutes per hour of audio
- Generate interactive HTML for manual review

## Backup Strategy
If LangExtract integration blocks, can:
1. Use simpler keyword extraction as fallback
2. Manual annotation of sample transcripts
3. Rule-based pattern matching for tool mentions

---
*Updated: Today's session - focusing on getting LangExtract working end-to-end*



