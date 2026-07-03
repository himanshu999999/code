"""
Codebase search and QA endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task import CodebaseQueryRequest, TaskResponse
from app.services.repository_service import RepositoryService
from app.workers.tasks import codebase_query_task

router = APIRouter()


@router.post("/query", response_model=TaskResponse, status_code=202)
async def query_codebase(
    request: CodebaseQueryRequest,
    db: Session = Depends(get_db),
):
    """
    Ask a question about the codebase.
    
    The system will:
    1. Retrieve relevant code chunks using hybrid search
    2. Generate an answer with citations
    3. Return task ID for async result retrieval
    
    Example questions:
    - "Where is authentication implemented?"
    - "Which files handle payment retries?"
    - "What is the request flow for login?"
    """
    service = RepositoryService(db)
    repo = service.get_repository(request.repository_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    if repo.status.value != "ready":
        raise HTTPException(
            status_code=400,
            detail=f"Repository not ready. Current status: {repo.status.value}"
        )
    
    # Create task record
    from app.models.task import Task, TaskType
    task = Task(
        repository_id=request.repository_id,
        task_type=TaskType.CODEBASE_QA,
        query=request.question,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Queue query task
    codebase_query_task.delay(task.id, request.question)
    
    return task


@router.post("/search")
async def search_code(
    query: str,
    repository_id: int,
    k: int = 10,
    db: Session = Depends(get_db),
):
    """
    Search code using hybrid retrieval (semantic + keyword).
    
    Returns ranked list of relevant code chunks with file paths and line numbers.
    """
    service = RepositoryService(db)
    repo = service.get_repository(repository_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Perform hybrid search
    results = service.search_code(query, repository_id, k=k)
    
    return {
        "query": query,
        "results": results,
        "total": len(results)
    }


@router.get("/{repo_id}/symbols")
async def list_symbols(
    repo_id: int,
    symbol_type: str = None,  # "class", "function", "import"
    db: Session = Depends(get_db),
):
    """
    List extracted symbols from a repository.
    
    Useful for understanding codebase structure and navigation.
    """
    service = RepositoryService(db)
    repo = service.get_repository(repo_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    symbols = service.get_symbols(repo_id, symbol_type=symbol_type)
    
    return {
        "repository_id": repo_id,
        "symbols": symbols
    }


@router.get("/{repo_id}/file/{file_path:path}")
async def get_file_content(
    repo_id: int,
    file_path: str,
    db: Session = Depends(get_db),
):
    """Get content of a specific file in the repository."""
    service = RepositoryService(db)
    repo = service.get_repository(repo_id)
    
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    content = service.get_file_content(repo_id, file_path)
    
    if not content:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "file_path": file_path,
        "content": content
    }
