"""
Repository management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.repository import Repository, RepoStatus
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryListResponse,
    IngestionProgress,
)
from app.services.repository_service import RepositoryService
from app.workers.tasks import ingest_repository_task

router = APIRouter()


@router.post("/ingest", response_model=RepositoryResponse, status_code=202)
async def ingest_repository(
    repo_data: RepositoryCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Start repository ingestion process.
    
    Clones the repository, parses files, extracts symbols, and creates embeddings.
    Returns immediately with PENDING status; ingestion happens asynchronously.
    """
    service = RepositoryService(db)
    
    # Create repository record
    repo = service.create_repository(
        url=str(repo_data.url),
        branch=repo_data.branch
    )
    
    # Queue ingestion task
    ingest_repository_task.delay(repo.id)
    
    return repo


@router.get("/", response_model=RepositoryListResponse)
async def list_repositories(
    skip: int = 0,
    limit: int = 20,
    status: RepoStatus = None,
    db: Session = Depends(get_db),
):
    """List all repositories with optional filtering."""
    service = RepositoryService(db)
    repos, total = service.list_repositories(skip=skip, limit=limit, status=status)
    
    return RepositoryListResponse(
        repositories=repos,
        total=total
    )


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: int,
    db: Session = Depends(get_db),
):
    """Get repository details by ID."""
    service = RepositoryService(db)
    repo = service.get_repository(repo_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return repo


@router.delete("/{repo_id}", status_code=204)
async def delete_repository(
    repo_id: int,
    db: Session = Depends(get_db),
):
    """Delete a repository and its indexed data."""
    service = RepositoryService(db)
    deleted = service.delete_repository(repo_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return None


@router.get("/{repo_id}/progress", response_model=IngestionProgress)
async def get_ingestion_progress(
    repo_id: int,
    db: Session = Depends(get_db),
):
    """Get current ingestion progress for a repository."""
    service = RepositoryService(db)
    repo = service.get_repository(repo_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Calculate progress based on status
    progress_map = {
        RepoStatus.PENDING: 0.0,
        RepoStatus.CLONING: 0.2,
        RepoStatus.PARSING: 0.5,
        RepoStatus.INDEXING: 0.8,
        RepoStatus.READY: 1.0,
        RepoStatus.FAILED: 0.0,
    }
    
    return IngestionProgress(
        status=repo.status.value,
        progress=progress_map.get(repo.status, 0.0),
        current_step=repo.status.value,
        message=f"Repository {repo.status.value}"
    )


@router.get("/{repo_id}/chunks", response_model=List[dict])
async def list_repository_chunks(
    repo_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List code chunks for a repository."""
    service = RepositoryService(db)
    repo = service.get_repository(repo_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    chunks = service.get_chunks(repo_id, skip=skip, limit=limit)
    return chunks
