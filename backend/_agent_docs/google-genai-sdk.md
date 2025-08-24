# Google GenAI SDK

We use the official **Google GenAI SDK** (`google-genai`) for all Gemini API interactions.

## Package
- **Current**: `google-genai==1.30.0` 
- **Deprecated**: `google-generativeai` (removed - EOL Nov 30, 2025)

## Why This SDK
- Official Google-supported SDK as of late 2024
- Unified interface for Gemini 2.5 Pro and Gemini 2.0 models
- Access to latest features (Live API, Veo, etc.)
- Better performance and actively maintained

## Usage
```python
from google import genai

client = genai.Client()  # Uses GEMINI_API_KEY env var
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Your prompt here"
)
```

## Migration Notes
- File uploads now use different API patterns
- Type hints simplified (no more `genai.File` issues)
- Authentication still uses `GEMINI_API_KEY` environment variable

## Documentation
- [Google GenAI SDK Docs](https://googleapis.github.io/python-genai/)
- [GitHub Repository](https://github.com/googleapis/python-genai)