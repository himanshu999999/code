"""
Shared utilities and constants for RepoPilot.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib


__version__ = "1.0.0"


class Language(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    C = "c"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    UNKNOWN = "unknown"


class TaskType(str, Enum):
    """Types of tasks RepoPilot can execute."""
    CODEBASE_QA = "codebase_qa"
    BUG_FIX = "bug_fix"
    CODE_REVIEW = "code_review"
    REFACTORING = "refactoring"
    TEST_GENERATION = "test_generation"
    DOCUMENTATION = "documentation"


@dataclass
class CodeSymbol:
    """Represents a code symbol (function, class, variable)."""
    name: str
    type: str  # function, class, method, variable, etc.
    file_path: str
    start_line: int
    end_line: int
    signature: Optional[str] = None
    docstring: Optional[str] = None
    parameters: Optional[List[str]] = None
    return_type: Optional[str] = None
    imports: Optional[List[str]] = None


@dataclass
class RetrievalResult:
    """Result from code retrieval operation."""
    file_path: str
    start_line: int
    end_line: int
    content: str
    score: float
    symbols: List[str]
    language: str


@dataclass
class PatchHunk:
    """A single hunk in a diff patch."""
    file_path: str
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    diff_text: str


@dataclass
class BugFixReport:
    """Complete report from a bug-fix operation."""
    issue_summary: str
    root_cause_hypothesis: str
    changed_files: List[str]
    patch_diff: str
    test_results: str
    confidence_score: float
    iterations: int
    failure_analysis: Optional[str] = None


LANGUAGE_EXTENSIONS = {
    Language.PYTHON: [".py", ".pyw"],
    Language.JAVASCRIPT: [".js", ".jsx", ".mjs"],
    Language.TYPESCRIPT: [".ts", ".tsx", ".mts"],
    Language.JAVA: [".java"],
    Language.GO: [".go"],
    Language.RUST: [".rs"],
    Language.CPP: [".cpp", ".cc", ".cxx", ".hpp", ".hxx"],
    Language.C: [".c", ".h"],
    Language.RUBY: [".rb"],
    Language.PHP: [".php"],
    Language.SWIFT: [".swift"],
    Language.KOTLIN: [".kt", ".kts"],
}

# Files and directories to ignore during indexing
IGNORE_PATTERNS = [
    ".git",
    ".svn",
    ".hg",
    "__pycache__",
    "node_modules",
    "vendor",
    "venv",
    ".venv",
    "env",
    ".env",
    "dist",
    "build",
    "target",
    "*.min.js",
    "*.bundle.js",
    "*.lock",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.so",
    "*.dll",
    "*.exe",
    "*.bin",
    "*.dat",
    "*.db",
    "*.sqlite",
    "*.log",
]

# Maximum chunk size for code indexing
MAX_CHUNK_SIZE = 512  # tokens (approximate)
CHUNK_OVERLAP = 50  # tokens

# Default retrieval parameters
DEFAULT_RETRIEVAL_K = 10
DEFAULT_CONFIDENCE_THRESHOLD = 0.7


def generate_chunk_id(file_path: str, start_line: int, end_line: int, content: str) -> str:
    """Generate a unique ID for a code chunk."""
    key = f"{file_path}:{start_line}:{end_line}:{content[:100]}"
    return hashlib.sha256(key.encode()).hexdigest()[:32]


def detect_language(file_path: str) -> Language:
    """Detect programming language from file extension."""
    ext = "." + file_path.split(".")[-1].lower() if "." in file_path else ""
    
    for lang, extensions in LANGUAGE_EXTENSIONS.items():
        if ext in extensions:
            return lang
    
    return Language.UNKNOWN


def is_ignored_path(path: str) -> bool:
    """Check if a path should be ignored during indexing."""
    import fnmatch
    import os
    
    path_parts = path.split(os.sep)
    
    for pattern in IGNORE_PATTERNS:
        # Check if any part of the path matches
        for part in path_parts:
            if fnmatch.fnmatch(part, pattern):
                return True
        
        # Check full path
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    
    return False


__all__ = [
    "Language",
    "TaskType",
    "CodeSymbol",
    "RetrievalResult",
    "PatchHunk",
    "BugFixReport",
    "LANGUAGE_EXTENSIONS",
    "IGNORE_PATTERNS",
    "MAX_CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "DEFAULT_RETRIEVAL_K",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "generate_chunk_id",
    "detect_language",
    "is_ignored_path",
    "__version__",
]
