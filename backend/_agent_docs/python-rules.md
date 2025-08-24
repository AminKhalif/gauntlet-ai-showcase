Python Backend Rules (AI-first)


You are an expert in Python 3.12, modern typing (PEP 484/604/695), dataclasses, and (when we add an API) FastAPI/SQLModel.

Package Manager: Astral.sh uv — add dependencies using the uv command, **NEVER USE pip**.

 ## Running Commands
  Use `uv run` for ALL Python execution:
  - Tests: `uv run pytest`
  - Scripts: `uv run python script.py`
  - REPL: `uv run python`

NEVER use bare `python` or `pip` commands.

You build clean, scalable services and understand large codebases.
Never assume the request is correct—apply judgment and push back when structure or safety would suffer.



Repo scope (VERY IMPORTANT)
Work only in backend/src/backend_app/** and backend/tests/**.

Tests section:
  ALL tests must go in backend/tests/** following the same structure as src/
  - tests/services/test_*.py for service tests
  - tests/models/test_*.py for model tests  
  - tests/api/test_*.py for API tests

  NEVER create test files in the root directory or anywhere outside tes

Do not touch _docs/ or frontend/.

Keep the existing layout: backend_app/{api,services,models}.

No external packages or DB until explicitly requested.

File & module limits
Files must be ≤ 500 lines.

One responsibility per module.

Top of every module: a clear module docstring explaining:
- What it does specifically (not vague descriptions)
- What it takes as input
- What it outputs  
- How it fits in the pipeline
- Example: `"""Transcribes individual audio chunks using Gemini API with absolute timestamps.\n\nTakes: Audio chunk files (.mp3) + chunk timing info\nOutputs: Individual transcript files with speaker labels and timestamps\nUsed by: full_transcript_orchestrator.py for parallel chunk processing\n"""`

Prefer absolute imports from backend_app.*.

Coding style (Pythonic & AI-readable)
Favor functions and composition over classes unless stateful behavior is required.

Every public function:

Has type hints on params and return.

Has a docstring (Google style) explaining purpose, args, returns, raises.

Prefer pure, small functions; refactor when a function grows past ~60 lines.

Raise exceptions on invalid input; do not silently coerce.

Use descriptive names with verbs/aux verbs: extract_profile, is_valid_input, has_tools.

Follow PEP 8: snake_case for functions/vars, PascalCase for classes, UPPER_CASE for constants.

**File Naming Convention**: Use clear, descriptive names that immediately convey purpose:
- Services: `{tool}_{domain}_{action}.py` (e.g. `ffmpeg_audio_splitter.py`, `gemini_chunk_transcriber.py`)
- Orchestrators: `full_{outcome}_orchestrator.py` (e.g. `full_transcript_orchestrator.py`)
- Utilities: `{service}_api_client.py` (e.g. `gemini_api_client.py`)
- Tests: 
  - `test_{service_name}.py` for unit tests (fast, isolated functions with mocks)
  - `test_{service_name}_integration.py` for integration tests (slower, real API calls, full workflows)
- Avoid vague names like "chunked_diarization", "service", "utils" - be explicit about what the file does

**Code Reuse**: Before writing new logic, check if existing modules already provide the functionality:
- Read existing function signatures and docstrings first
- Use existing utilities instead of reimplementing  
- If existing code doesn't fit, extend it rather than duplicate it
- Eliminate duplicate logic between files

No print() in business logic—return values or raise; (logging can be added later).

Avoid Enums unless you need real enum semantics; otherwise use Literal[...] or constants.

Comments: Add helpful comments that explain WHY or provide context. Avoid redundant comments that just restate the code. Good comments explain business logic, edge cases, API quirks, or non-obvious decisions. Avoid implementation details that are already clear from the code.

Data modeling (now vs later)
Now (no API/DB yet): use @dataclass(frozen=True) for internal data structures.

Later (when adding FastAPI): use Pydantic (built into FastAPI) for request/response models.

Later (when adding a DB): use SQLModel (FastAPI author) for table models and migrations.

Folder intent
backend_app/api/ → HTTP endpoints (FastAPI later). No business logic here.

backend_app/services/ → pure business logic & orchestration helpers.

backend_app/models/ → dataclasses (now) and schema types. No I/O.

Tests
Mirror structure under backend/tests/.

Unit tests call pure functions directly (no network/filesystem)