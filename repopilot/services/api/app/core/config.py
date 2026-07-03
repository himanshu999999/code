"""
Application configuration and settings.

Uses pydantic-settings for environment variable management with validation.
"""

from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    DEBUG: bool = Field(default=False, description="Debug mode")
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT and encryption"
    )
    APP_NAME: str = "RepoPilot"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/repopilot",
        description="PostgreSQL connection string"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string"
    )
    
    # ChromaDB
    CHROMA_HOST: str = Field(default="localhost", description="ChromaDB host")
    CHROMA_PORT: int = Field(default=8000, description="ChromaDB port")
    
    # LLM Configuration
    LLM_PROVIDER: str = Field(
        default="openai",
        description="LLM provider: openai, anthropic, ollama"
    )
    LLM_API_KEY: Optional[str] = Field(default=None, description="LLM API key")
    LLM_MODEL: str = Field(
        default="gpt-4-turbo-preview",
        description="LLM model name"
    )
    LLM_TEMPERATURE: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="LLM temperature"
    )
    LLM_MAX_TOKENS: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens for LLM responses"
    )
    
    # GitHub (optional)
    GITHUB_TOKEN: Optional[str] = Field(default=None, description="GitHub API token")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=100,
        description="API rate limit per minute"
    )
    MAX_CONCURRENT_LLM_CALLS: int = Field(
        default=10,
        description="Maximum concurrent LLM calls"
    )
    MAX_SANDBOX_EXECUTIONS: int = Field(
        default=5,
        description="Maximum parallel sandbox executions"
    )
    
    # Sandbox
    SANDBOX_TIMEOUT: int = Field(
        default=300,
        description="Sandbox execution timeout in seconds"
    )
    SANDBOX_MEMORY_LIMIT: str = Field(
        default="512m",
        description="Sandbox memory limit"
    )
    WORKSPACE_DIR: str = Field(
        default="/tmp/repo_workspaces",
        description="Directory for repo workspaces"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format: json or console")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    @property
    def chroma_url(self) -> str:
        """Get full ChromaDB URL."""
        return f"http://{self.CHROMA_HOST}:{self.CHROMA_PORT}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
