"""
Pydantic schemas for repository operations.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RepoStatusEnum(str, Enum):
    PENDING = "pending"
    CLONING = "cloning"
    PARSING = "parsing"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"


class RepositoryCreate(BaseModel):
    """Schema for creating a repository."""
    url: HttpUrl = Field(..., description="GitHub repository URL")
    branch: str = Field(default="main", description="Branch to clone")


class RepositoryResponse(BaseModel):
    """Schema for repository response."""
    id: int
    name: str
    url: str
    branch: str
    status: RepoStatusEnum
    language: Optional[str] = None
    total_files: int = 0
    total_chunks: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RepositoryListResponse(BaseModel):
    """Schema for listing repositories."""
    repositories: List[RepositoryResponse]
    total: int


class CodeChunkResponse(BaseModel):
    """Schema for code chunk response."""
    id: int
    file_path: str
    start_line: int
    end_line: int
    content: str
    symbols: Optional[List[str]] = None
    imports: Optional[List[str]] = None
    language: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class IngestionProgress(BaseModel):
    """Schema for ingestion progress."""
    status: str
    progress: float = Field(ge=0.0, le=1.0)
    current_step: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None
