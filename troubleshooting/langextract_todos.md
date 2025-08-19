# LangExtract Integration Research & TODOs

## Project Context
We're building an AI workflow showcase app that extracts structured information from podcast/transcript data about how AI builders create software. We need to parse raw transcripts (with timestamps and speaker identification) into organized workflow categories.

## Current Pipeline Status
- ✅ YouTube MP3 download
- ✅ Speech-to-text transcription with timestamps
- ✅ Speaker diarization
- ⏳ **NEXT**: Structured data extraction using LangExtract

## LangExtract Research Goals

### 1. Core Library Understanding
- **Purpose**: LangExtract uses LLMs to extract structured information from unstructured text documents
- **Key Features**: 
  - Schema-based extraction with user-defined instructions
  - **Source location mapping** (exact text locations) - **CRITICAL for timestamp correlation**
  - Few-shot learning with examples for consistent output
  - LLM integration (OpenAI, Google Gemini, Ollama local models)
  - Python-native implementation
  - **JSONL output format** for easy processing
  - **Interactive HTML visualizations** for results
- **Relevance**: Perfect for converting raw transcripts into structured workflow profiles
- **Trust Score**: 8.9/10 (highly authoritative)
- **Version**: v1.0.7 (latest)

### 2. Target Workflow Categories
Based on project-overview.md, we need to extract:
- **Planning & Scoping**: Goals, constraints, requirements definition
- **Context Management**: Prompt structuring, memory management, information organization
- **Guardrails & Validation**: Testing, reviews, quality assurance
- **Iteration Style**: Refinement, testing, evolution patterns
- **Tool Stack**: Tools used, categorized by role and purpose
- **Integration & Orchestration**: AI-tool connections, API usage, system integration
- **Deployment & Delivery**: Demo to production processes

### 3. Data Extraction Strategy

#### Input Format
- Raw transcript text with timestamps
- Speaker identification
- Potentially messy, conversational language

#### Output Format
- Structured JSON matching workflow categories
- Extracted quotes and examples
- Tool lists with categorization
- Timestamp mapping to workflow sections

#### Extraction Patterns
- **Goal Identification**: "I wanted to build...", "The main challenge was...", "The goal was to..."
- **Process Descriptions**: "First I...", "Then I tried...", "I realized...", "I started by..."
- **Tool Mentions**: "I used...", "I integrated with...", "The API for...", "I switched to..."
- **Validation Steps**: "I tested...", "I reviewed...", "I made sure...", "I validated..."
- **Iteration Patterns**: "I went back and...", "I refined...", "I improved..."
- **Deployment Steps**: "I deployed...", "I launched...", "I shared..."

### 4. Integration Architecture

#### Current Pipeline
```
YouTube → MP3 → STT + Timestamps → Diarization → [NEW: LangExtract] → Structured Workflow
```

#### LangExtract Integration Points
- **Input**: Cleaned transcript text (speaker + content + timestamps)
- **Processing**: LLM-powered extraction with defined schemas and few-shot examples
- **Output**: Structured workflow data with **exact source locations** for timestamp correlation
- **Format**: JSONL files for easy processing and HTML visualizations for review

### 5. Implementation Considerations

#### Schema Design
- Define extraction schemas for each workflow category
- Handle optional/missing information gracefully
- Support for nested data (tools within categories)

#### LLM Integration
- **Recommended Model**: `gemini-2.5-flash` (balance of speed, cost, quality)
- **Alternative Models**: `gpt-4o`, `llama3` (via Ollama for local processing)
- **Prompt Engineering**: Clear extraction instructions + high-quality few-shot examples
- **Cost Optimization**: 
  - Use `extraction_passes=3` for better recall
  - Implement `max_char_buffer=1000` for chunked processing
  - Use `max_workers=20` for parallel processing

#### Data Quality
- Handling incomplete or unclear transcript sections
- Confidence scoring for extracted information
- Fallback strategies for extraction failures

## Next Steps (TODOs)

### Phase 1: Research & Setup
- [x] Test Context7 MCP functionality
- [x] Resolve library ID and basic information
- [x] Access full documentation via Context7 MCP
- [x] Review code examples and usage patterns
- [x] Identify optimal extraction schemas
- [x] Research LLM options and costs

### Phase 2: Schema Design
- [ ] Design JSON schema for workflow extraction
- [ ] Create extraction prompts for each category
- [ ] Define validation rules for extracted data
- [ ] Plan error handling and fallbacks

### Phase 3: Integration Planning
- [ ] Design integration with existing transcript pipeline
- [ ] Plan data flow from diarization to extraction
- [ ] Consider caching and optimization strategies
- [ ] Plan testing and validation approach

### Phase 4: Implementation
- [ ] Implement LangExtract service
- [ ] Integrate with existing backend
- [ ] Add extraction endpoints to API
- [ ] Create test cases and validation

## Questions to Resolve
1. **LLM Choice**: ✅ **Resolved** - Use `gemini-2.5-flash` for best balance
2. **Schema Flexibility**: ✅ **Resolved** - Use few-shot examples for consistent output
3. **Performance**: ✅ **Resolved** - Use chunked processing with parallel workers
4. **Fallback Strategy**: ✅ **Resolved** - Multiple extraction passes improve recall
5. **Source Mapping**: ✅ **Resolved** - Built-in character position tracking for timestamps

## MCP Integration Status
- ✅ **resolve-library-id**: Working - Successfully found `/google/langextract`
- ✅ **get-library-docs**: Now working - Retrieved comprehensive documentation
- ✅ **Research Complete**: All critical information gathered via MCP

## Resources
- [LangExtract Documentation](https://github.com/google/langextract)
- [Context7 MCP Integration] ✅ Working
- [Project Overview](../_docs/project-overview.md)

## Implementation Plan (Based on Research)

### 1. Core Extraction Schema for Workflows
```python
# Example extraction classes for your workflow categories
extraction_classes = [
    "planning_goal",      # Goals, constraints, requirements
    "context_strategy",   # Prompt structuring, memory management
    "guardrail_method",   # Testing, validation, quality assurance
    "iteration_pattern",  # Refinement, evolution, testing cycles
    "tool_usage",        # Tools, APIs, integrations mentioned
    "orchestration",     # AI-tool connect=ions, workflows
    "deployment_step"    # Demo, launch, sharing processes
]
```

### 2. Few-Shot Examples Structure
- **Input**: Transcript segments with speaker + content + timestamps
- **Output**: Structured extractions with attributes linking to workflow categories
- **Key**: Use real examples from your existing transcripts to train the model

### 3. Integration with Your Pipeline
```
YouTube → MP3 → STT + Timestamps → Diarization → LangExtract → Structured Workflow
                                                      ↓
                                              JSONL + HTML Visualization
```

### 4. Technical Implementation
- **Model**: `gemini-2.5-flash` with API key
- **Processing**: Chunked with `max_char_buffer=1000`
- **Parallelization**: `max_workers=20` for speed
- **Quality**: `extraction_passes=3` for better recall
- **Output**: JSONL files + interactive HTML visualizations

### 5. Next Implementation Steps
1. **Install LangExtract**: `pip install langextract`
2. **Set up API key**: `export LANGEXTRACT_API_KEY="your-key"`
3. **Create extraction schemas** for your workflow categories
4. **Build few-shot examples** from sample transcripts
5. **Integrate with existing diarization service**
6. **Test with small transcript samples**
7. **Scale to full pipeline integration**

---
*Last Updated: December 2024*
*Status: Research Complete - Ready for Implementation*
*MCP Research: ✅ Successful via Context7*

## Research Summary

**LangExtract is PERFECT for your AI workflow showcase project!** Here's why:

✅ **Source Location Mapping**: Automatically maps extracted workflow elements to exact transcript positions (perfect for timestamp correlation)

✅ **Few-Shot Learning**: Uses examples to ensure consistent extraction of your 7 workflow categories

✅ **LLM Integration**: Works with Gemini, OpenAI, or local Ollama models

✅ **Structured Output**: JSONL format that's easy to process and visualize

✅ **Performance Optimized**: Chunked processing with parallel workers for large transcripts

✅ **Interactive Results**: Built-in HTML visualizations for reviewing extracted workflows

**Next**: Move to Phase 2 (Schema Design) and start building your extraction schemas!


---

## Implementation Blueprint (AI-readable, project-specific)

This section is prescriptive so another AI agent can implement extraction end-to-end without additional clarification. It translates research into concrete schemas, prompts, mapping logic, service APIs, data models, parameters, and tests.

### A. Extraction Schema (classes and attributes)
- planning_goal: attributes {goal_type?, metric?, constraint?}
- acceptance_criterion: attributes {metric?, scope?, testable?: "yes"|"no"}
- context_strategy: attributes {technique: "prompt_structuring"|"memory"|"chunking"|"linking", artifact?}
- guardrail: attributes {type: "tests"|"reviews"|"constraints"|"validation", tool?}
- iteration_pattern: attributes {pattern: "tight_loop"|"compare_alternatives"|"replay_edge_cases", cadence?}
- tool_usage: attributes {tool_name, category: "gen"|"editor"|"testing"|"api_debug"|"orchestration"|"code_completion", role?}
- orchestration: attributes {pattern: "api+llm"|"tool_chain"|"deterministic_flow", tools?}
- deployment_step: attributes {step: "demo"|"share"|"release"|"ci_check", env?}
- quote: attributes {topic: one of the categories above}

Rules for the extractor:
- Extract entities in order of appearance; use exact source spans; do not paraphrase; do not overlap spans.
- Prefer concrete examples over abstract advice; only label when explicitly stated.

### B. Prompt Template (final form used with LangExtract)
```python
prompt = """
You are extracting how a builder works with AI from a transcript with speakers.

Extract entities in order of appearance using exact text spans (no paraphrasing). Do not overlap spans.

Classes and required attributes:
- planning_goal {goal_type?, metric?, constraint?}
- acceptance_criterion {metric?, scope?, testable?}
- context_strategy {technique, artifact?}
- guardrail {type, tool?}
- iteration_pattern {pattern, cadence?}
- tool_usage {tool_name, category, role?}
- orchestration {pattern, tools?}
- deployment_step {step, env?}
- quote {topic}

Guidelines:
- When a tool is named (e.g., "Jest", "Postman", "LangChain", "Cursor", "GPT-4o"), emit tool_usage with category and role if stated.
- If a sentence implies validation with tests, emit guardrail {type:"tests"} and link the exact span.
- Keep spans short and precise; use speaker’s exact words.
"""
```

### C. Few‑Shot Examples (domain-specific)
```python
examples = [
  lx.data.ExampleData(
    text="HOST: Let's define success.\nJANE: Summarize goals and propose 3–5 checkpoints we can verify with tests.",
    extractions=[
      lx.data.Extraction(
        extraction_class="planning_goal",
        extraction_text="Summarize goals and propose 3–5 checkpoints we can verify with tests",
        attributes={"goal_type":"spec-first","metric":"checkpoints"}
      ),
      lx.data.Extraction(
        extraction_class="guardrail",
        extraction_text="verify with tests",
        attributes={"type":"tests","tool":"Jest"}
      ),
    ],
  ),
  lx.data.ExampleData(
    text="JANE: Prefer minimal prompts, code-level validation, and repeatable orchestration.",
    extractions=[
      lx.data.Extraction(
        extraction_class="context_strategy",
        extraction_text="minimal prompts",
        attributes={"technique":"prompt_structuring"}
      ),
      lx.data.Extraction(
        extraction_class="guardrail",
        extraction_text="code-level validation",
        attributes={"type":"tests"}
      ),
      lx.data.Extraction(
        extraction_class="orchestration",
        extraction_text="repeatable orchestration",
        attributes={"pattern":"tool_chain"}
      ),
    ],
  ),
  lx.data.ExampleData(
    text="We use Cursor for inline diffs and GPT‑4o for code generation; Postman verifies endpoints.",
    extractions=[
      lx.data.Extraction(
        extraction_class="tool_usage",
        extraction_text="Cursor",
        attributes={"tool_name":"Cursor","category":"editor","role":"inline diffs"}
      ),
      lx.data.Extraction(
        extraction_class="tool_usage",
        extraction_text="GPT‑4o",
        attributes={"tool_name":"GPT‑4o","category":"gen","role":"code generation"}
      ),
      lx.data.Extraction(
        extraction_class="tool_usage",
        extraction_text="Postman",
        attributes={"tool_name":"Postman","category":"api_debug","role":"verify endpoints"}
      ),
    ],
  ),
]
```

### D. Transcript → Timestamp Mapping
Input: diarized `segments: list[TranscriptSegment]` with fields `{start_s: float, end_s: float, speaker: str, text: str}`.

Procedure:
1. Concatenate `segments[i].text` into `full_text`, store `segments[i].cum_start_char` (cumulative char offset of each segment in the concatenated string).
2. Run `lx.extract` on `full_text`.
3. For each `Extraction` with `char_interval.start_pos/end_pos`:
   - Find segment `k` where `cum_start_char[k] <= start_pos < cum_start_char[k] + len(text_k)` (binary search over offsets).
   - Compute `char_in_seg = start_pos - cum_start_char[k]` and interpolate time:
     `t_start = start_s[k] + (char_in_seg / max(1, len(text_k))) * (end_s[k] - start_s[k])`.
   - Repeat for `end_pos` to get `t_end`.
   - Attach `speaker = segments[k].speaker`.

### E. Service APIs (backend/src/backend_app/services/langextract.py)
- `build_prompt() -> str`
- `build_few_shot_examples() -> list[lx.data.ExampleData]`
- `run_langextract_on_transcript(segments: list[TranscriptSegment], model_id: str = "gemini-2.5-flash", extraction_passes: int = 3, max_workers: int = 20, max_char_buffer: int = 1000) -> LangExtractResult`
  - Concatenate text, call `lx.extract`, return result and mapping table.
- `to_workflow_entities(result: LangExtractResult, segments: list[TranscriptSegment]) -> list[WorkflowEntity]`
  - Map char intervals to timestamps + speaker; normalize attributes per schema.
- `group_into_profile(entities: list[WorkflowEntity]) -> WorkflowProfile`
  - Aggregate into sections used by the UI.

### F. Data Models (backend/src/backend_app/models)
- `TranscriptSegment`: `{start_s: float, end_s: float, speaker: str, text: str}`
- `WorkflowEntity`: `{category: Literal[...], text: str, start_s: float, end_s: float, speaker: str|None, attributes: dict}`
- `WorkflowProfile`: `{planning_goals, context_management, guardrails, iteration_style, tools, orchestration, deployment, quotes}` (each a list of `WorkflowEntity` or summarized forms)

### G. LangExtract Call Parameters (defaults)
- `model_id="gemini-2.5-flash"`
- `extraction_passes=3`
- `max_workers=20`
- `max_char_buffer=1000`

### H. Artifacts for Review
- Save JSONL: `lx.io.save_annotated_documents([result], output_name="workflow_extractions.jsonl", output_dir=".")`
- Visualization HTML: `html = lx.visualize("workflow_extractions.jsonl")`

### I. Tests (no external network; mock lx)
Create under `backend/tests/services/`:
- `test_langextract_mapping.py`: Validate char→timestamp mapping across boundaries using synthetic segments.
- `test_langextract_grouping.py`: Given mocked `Extraction` objects, assert grouping into `WorkflowProfile` by categories and attributes.
- `test_langextract_examples_valid.py`: Ensure few‑shot examples have non-overlapping spans and required attributes.

### J. Tooling and Constraints (repo rules)
- Dependency management only via uv: `uv add langextract` (do not use pip).
- Execute scripts and tests with `uv run`.
- Keep modules ≤ 500 lines; functions small with full type hints and Google-style docstrings.

### K. Pipeline Placement
`YouTube → MP3 → STT + Timestamps → Diarization → LangExtract (this blueprint) → Structured Workflow JSON → UI`

### L. Actionable Next Steps
1. Add data models and service skeletons (no network).
2. Implement mapping utilities and grouping logic.
3. Add unit tests with mocks; ensure green.
4. After approval, `uv add langextract`; integrate real call behind a feature flag.
5. Generate JSONL + HTML artifacts for manual review on a small transcript sample.
