"""
Pydantic schemas for task operations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TaskTypeEnum(str, Enum):
    CODEBASE_QA = "codebase_qa"
    BUG_FIX = "bug_fix"
    EVALUATION = "evaluation"


class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CodebaseQueryRequest(BaseModel):
    """Schema for codebase QA request."""
    question: str = Field(..., min_length=1, max_length=2000, description="Question about the codebase")
    repository_id: int = Field(..., description="Repository ID to query")


class BugFixRequest(BaseModel):
    """Schema for bug fix request."""
    issue_description: str = Field(..., min_length=10, max_length=5000, description="Bug description or issue")
    repository_id: int = Field(..., description="Repository ID")
    test_command: Optional[str] = Field(None, description="Command to run tests")


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    repository_id: int
    task_type: TaskTypeEnum
    status: TaskStatusEnum
    query: str
    test_command: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    confidence_score: Optional[float] = None
    latency_ms: Optional[int] = None
    token_usage: Optional[int] = None
    celery_task_id: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for listing tasks."""
    tasks: List[TaskResponse]
    total: int


class TaskResult(BaseModel):
    """Schema for task result data."""
    answer: Optional[str] = None
    cited_files: Optional[List[Dict[str, Any]]] = None
    patch: Optional[str] = None
    changed_files: Optional[List[str]] = None
    test_output: Optional[str] = None
    confidence_score: Optional[float] = None
    iterations: Optional[int] = None
