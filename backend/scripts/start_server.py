"""Start FastAPI development server for AI Workflow Showcase.

Simple script to run the FastAPI server with proper imports and hot reload.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
backend_root = Path(__file__).parent.parent
src_path = backend_root / "src"
sys.path.insert(0, str(src_path))

import uvicorn


def main():
    """Start the FastAPI development server."""
    print("🚀 Starting AI Workflow Showcase API server...")
    print("📍 Server will be available at: http://localhost:8001")
    print("🔄 Auto-reload enabled for development")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(
        "backend_app.api.fastapi_server:app",
        host="127.0.0.1", 
        port=8001,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()