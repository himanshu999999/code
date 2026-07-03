"""
Task model for tracking bug-fix and QA operations.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, enum.Enum):
    CODEBASE_QA = "codebase_qa"
    BUG_FIX = "bug_fix"
    EVALUATION = "evaluation"


class Task(Base):
    """Task model for tracking bug-fix and QA operations."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Task information
    task_type = Column(SQLEnum(TaskType), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    
    # Input
    query = Column(Text, nullable=False)
    test_command = Column(String(512))
    
    # Output
    result = Column(JSON)
    error_message = Column(Text)
    
    # Metrics
    confidence_score = Column(Float)
    latency_ms = Column(Integer)
    token_usage = Column(Integer)
    
    # Celery task ID for async tracking
    celery_task_id = Column(String(255), index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    repository = relationship("Repository", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, type={self.task_type}, status={self.status})>"
