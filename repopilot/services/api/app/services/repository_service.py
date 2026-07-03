"""
Repository service for business logic.
"""

from sqlalchemy.orm import Session
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import re

from app.models.repository import Repository, CodeChunk, RepoStatus


class RepositoryService:
    """Service class for repository operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_repository(self, url: str, branch: str = "main") -> Repository:
        """Create a new repository record."""
        # Extract repo name from URL
        name_match = re.search(r'/([^/]+/[^/]+?)(?:\.git)?$', url)
        name = name_match.group(1) if name_match else url
        
        repo = Repository(
            name=name,
            url=url,
            branch=branch,
            status=RepoStatus.PENDING
        )
        
        self.db.add(repo)
        self.db.commit()
        self.db.refresh(repo)
        
        return repo
    
    def get_repository(self, repo_id: int) -> Optional[Repository]:
        """Get repository by ID."""
        return self.db.query(Repository).filter(Repository.id == repo_id).first()
    
    def list_repositories(
        self,
        skip: int = 0,
        limit: int = 20,
        status: RepoStatus = None
    ) -> Tuple[List[Repository], int]:
        """List repositories with pagination and filtering."""
        query = self.db.query(Repository)
        
        if status:
            query = query.filter(Repository.status == status)
        
        total = query.count()
        repos = query.order_by(Repository.created_at.desc()).offset(skip).limit(limit).all()
        
        return repos, total
    
    def delete_repository(self, repo_id: int) -> bool:
        """Delete repository and all associated data."""
        repo = self.get_repository(repo_id)
        
        if not repo:
            return False
        
        # Delete chunks (cascade will handle this)
        self.db.delete(repo)
        self.db.commit()
        
        return True
    
    def update_status(self, repo_id: int, status: RepoStatus) -> Repository:
        """Update repository status."""
        repo = self.get_repository(repo_id)
        
        if repo:
            repo.status = status
            repo.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(repo)
        
        return repo
    
    def update_metadata(
        self,
        repo_id: int,
        language: str = None,
        total_files: int = None,
        total_chunks: int = None
    ) -> Repository:
        """Update repository metadata."""
        repo = self.get_repository(repo_id)
        
        if repo:
            if language:
                repo.language = language
            if total_files is not None:
                repo.total_files = total_files
            if total_chunks is not None:
                repo.total_chunks = total_chunks
            
            repo.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(repo)
        
        return repo
    
    def get_chunks(
        self,
        repo_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[CodeChunk]:
        """Get code chunks for a repository."""
        return (
            self.db.query(CodeChunk)
            .filter(CodeChunk.repository_id == repo_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_code(
        self,
        query: str,
        repo_id: int,
        k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search code using hybrid retrieval.
        
        TODO: Implement actual vector + keyword search with ChromaDB.
        For now, returns mock results.
        """
        # Placeholder - will be implemented with actual retrieval engine
        chunks = (
            self.db.query(CodeChunk)
            .filter(CodeChunk.repository_id == repo_id)
            .limit(k)
            .all()
        )
        
        return [
            {
                "file_path": chunk.file_path,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content[:200] + "...",
                "symbols": chunk.symbols,
                "score": 0.9 - (i * 0.05)  # Mock score
            }
            for i, chunk in enumerate(chunks)
        ]
    
    def get_symbols(
        self,
        repo_id: int,
        symbol_type: str = None
    ) -> List[Dict[str, Any]]:
        """Get extracted symbols from repository."""
        chunks = (
            self.db.query(CodeChunk)
            .filter(CodeChunk.repository_id == repo_id)
            .filter(CodeChunk.symbols != None)
            .all()
        )
        
        symbols = []
        for chunk in chunks:
            for symbol in (chunk.symbols or []):
                symbols.append({
                    "name": symbol,
                    "file_path": chunk.file_path,
                    "line": chunk.start_line,
                    "type": "function"  # Would need proper type detection
                })
        
        return symbols
    
    def get_file_content(
        self,
        repo_id: int,
        file_path: str
    ) -> Optional[str]:
        """Get content of a specific file."""
        chunks = (
            self.db.query(CodeChunk)
            .filter(CodeChunk.repository_id == repo_id)
            .filter(CodeChunk.file_path == file_path)
            .order_by(CodeChunk.start_line)
            .all()
        )
        
        if not chunks:
            return None
        
        # Reconstruct file from chunks
        return "\n".join(chunk.content for chunk in chunks)
