# Gauntlet AI — Workflow Showcase

Gauntlet AI showcases how engineers ship software with an AI-first approach, where the model writes most of the code and the engineer steers.

## What this does

- **Ingests podcast interviews** with AI builders discussing their workflows
- **Transcribes and diarizes** audio into structured speaker segments  
- **Extracts comparable workflow cards** using LangExtract to identify patterns
- **Presents unified profiles** that let you compare how different builders work

## Six workflow cards extracted

1. **Planning & Scoping** - Goals, constraints, definition of done
2. **Context Management** - How they prep and feed info to models
3. **Codegen Loop** - How they steer the model to write code
4. **Verification & Safeguards** - How they check output before it lands
5. **Iteration Style** - How they evolve solutions over time
6. **Deployment & Delivery** - How changes reach users

## Project Structure

- **[_docs/](_docs/)** - Documentation and project specifications
- **[frontend/](frontend/)** - Next.js application for browsing workflow profiles
- **[backend/](backend/)** - Python pipeline: audio processing → transcription → extraction

## Getting Started

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
uv sync
uv run python -m pytest  # Run tests
```

See [backend/README.md](backend/README.md) for detailed setup.

## How it works

```
YouTube Podcast → MP3 → Transcription → Diarization → LangExtract → Workflow Cards
```

The backend processes audio files through Google's Gemini for transcription and uses LangExtract to identify and extract workflow patterns into structured, comparable profiles.

## Documentation

See [_docs/](_docs/) for detailed project documentation including:
- [Project Overview](_docs/project-overview.md)
- [Project Roadmap](_docs/PROJECT-ROADMAP.md)
- [System Architecture](_docs/SYSTEM-ARCHITECTURE.md)