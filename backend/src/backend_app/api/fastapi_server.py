"""FastAPI server application for AI Workflow Showcase backend.

Takes: HTTP requests from Next.js frontend
Outputs: JSON API responses with proper status codes
Used by: Frontend API routes for all backend operations

Main FastAPI application with all route handlers and middleware.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .fastapi_builders_routes import router as builders_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Workflow Showcase API",
    description="Backend API for builder workflow processing and management",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Workflow Showcase API",
        "version": "1.0.0"
    }


@app.get("/health")
async def detailed_health_check() -> dict:
    """Detailed health check with service status."""
    try:
        # TODO: Add database connectivity check
        return {
            "status": "healthy",
            "services": {
                "database": "connected",  # Will implement actual check
                "gcs": "available",
                "langextract": "available"
            },
            "timestamp": "2025-01-01T00:00:00Z"  # Will add real timestamp
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Include route handlers
app.include_router(builders_router)


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting AI Workflow Showcase API server...")
    uvicorn.run(
        "fastapi_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )