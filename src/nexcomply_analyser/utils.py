"""Utility functions for file handling and logging."""

import logging
from pathlib import Path
from typing import List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def get_project_root() -> Path:
    """Get the project root directory.
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent.parent


def get_data_dir(subfolder: str) -> Path:
    """Get path to a data directory in the project.
    
    Args:
        subfolder: Name of the subfolder (e.g., 'Questionnaires')
        
    Returns:
        Path to the data directory
    """
    root = get_project_root()
    data_path = root / subfolder
    return data_path


def list_files(directory: Path, extensions: Optional[List[str]] = None) -> List[Path]:
    """List files in a directory with optional extension filter.
    
    Args:
        directory: Directory to list files from
        extensions: List of extensions to filter (e.g., ['.xlsx', '.pdf'])
        
    Returns:
        List of file paths
    """
    if not directory.exists():
        return []
    
    files = []
    for item in directory.iterdir():
        if item.is_file():
            if extensions is None or item.suffix.lower() in extensions:
                files.append(item)
    
    return sorted(files)


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        Path to the directory
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
