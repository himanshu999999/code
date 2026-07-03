"""
Shared utilities and constants for RepoPilot.
"""

__version__ = "1.0.0"

# Common constants
SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "go",
    "java",
    "rust",
    "cpp",
    "c",
]

DEFAULT_CHUNK_SIZE = 500  # lines
DEFAULT_CHUNK_OVERLAP = 50  # lines

# Ignore patterns for repo ingestion
IGNORE_PATTERNS = [
    ".git/",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    ".env",
    "*.log",
    "dist/",
    "build/",
    "vendor/",
    "*.min.js",
    "*.bundle.js",
]
