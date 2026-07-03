"""
Evaluation run model for benchmark results.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EvaluationRun(Base):
    """Evaluation run model for benchmark results."""
    
    __tablename__ = "evaluation_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Configuration
    dataset_name = Column(String(100), nullable=False)
    metrics = Column(JSON, default=list)
    
    # Results
    results = Column(JSON)
    summary = Column(JSON)
    
    # Status
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<EvaluationRun(dataset='{self.dataset_name}', status={self.status})>"
