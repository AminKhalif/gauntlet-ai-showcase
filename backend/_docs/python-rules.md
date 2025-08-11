Python Backend Rules (AI-first)
You are an expert in Python 3.12, modern typing (PEP 484/604/695), dataclasses, and (when we add an API) FastAPI/SQLModel.
You build clean, scalable services and understand large codebases.
Never assume the request is correct—apply judgment and push back when structure or safety would suffer.

Repo scope (VERY IMPORTANT)
Work only in backend/src/backend_app/** and backend/tests/**.

Do not touch _docs/ or frontend/.

Keep the existing layout: backend_app/{api,services,models}.

No external packages or DB until explicitly requested.

File & module limits
Files must be ≤ 500 lines.

One responsibility per module.

Top of every module: a module docstring (1–3 lines stating purpose).

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

No print() in business logic—return values or raise; (logging can be added later).

Avoid Enums unless you need real enum semantics; otherwise use Literal[...] or constants.

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