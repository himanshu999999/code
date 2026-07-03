"""
RepoPilot API - FastAPI Backend Service

This service provides REST APIs for:
- Repository ingestion and management
- Codebase search and QA
- Bug-fix agent orchestration
- Evaluation execution
- Run history tracking
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.api.v1 import repos, codebase, issues, evaluations, health
from app.core.logging import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title="RepoPilot API",
    description="AI-powered codebase intelligence and autonomous bug-fix platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "unhandled_exception",
        path=str(request.url.path),
        method=request.method,
        error=str(exc)
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_type": type(exc).__name__}
    )

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(repos.router, prefix="/api/v1/repos", tags=["Repositories"])
app.include_router(codebase.router, prefix="/api/v1/codebase", tags=["Codebase"])
app.include_router(issues.router, prefix="/api/v1/issues", tags=["Issues"])
app.include_router(evaluations.router, prefix="/api/v1/evaluations", tags=["Evaluations"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "RepoPilot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("application_startup", service="repopilot-api")
    # Initialize database connections, etc.

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("application_shutdown", service="repopilot-api")
    # Cleanup connections, etc.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
