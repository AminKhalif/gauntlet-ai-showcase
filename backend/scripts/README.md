# Backend Scripts

## start_server.py
Starts the FastAPI development server on http://localhost:8001

Usage:
```bash
cd backend
uv run python scripts/start_server.py
```

Server will auto-reload on code changes.

## Troubleshooting

**If you get "Address already in use" error:**
```bash
# Option 1: Kill any running servers first
pkill -f uvicorn

# Option 2: If that doesn't work, kill by port number
lsof -ti:8001 | xargs kill -9

# Then start the server
uv run python scripts/start_server.py
```

**To stop the server:**
- Press `Ctrl+C` in the terminal where it's running
- Or if running in background: `pkill -f uvicorn`

**Check if server is running:**
```bash
curl http://localhost:8001/health
```