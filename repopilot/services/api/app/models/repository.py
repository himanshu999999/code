"""
Repository and CodeChunk models.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class RepoStatus(str, enum.Enum):
    PENDING = "pending"
    CLONING = "cloning"
    PARSING = "parsing"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"


class Repository(Base):
    """Repository model representing an indexed codebase."""
    
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    url = Column(String(512), nullable=False)
    branch = Column(String(100), default="main")
    status = Column(SQLEnum(RepoStatus), default=RepoStatus.PENDING)
    
    # Metadata
    language = Column(String(50))
    total_files = Column(Integer, default=0)
    total_chunks = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    chunks = relationship("CodeChunk", back_populates="repository", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="repository", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Repository(id={self.id}, name='{self.name}', status={self.status})>"


class CodeChunk(Base):
    """Code chunk model for indexed code segments."""
    
    __tablename__ = "code_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False, index=True)
    
    # File information
    file_path = Column(String(512), nullable=False, index=True)
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    
    # Symbols and metadata
    symbols = Column(JSON, default=list)
    imports = Column(JSON, default=list)
    language = Column(String(50))
    
    # Embedding reference
    embedding_id = Column(String(255), index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    repository = relationship("Repository", back_populates="chunks")
    
    def __repr__(self):
        return f"<CodeChunk(file='{self.file_path}', lines={self.start_line}-{self.end_line})>"
