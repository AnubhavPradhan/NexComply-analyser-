"""Text parsing and normalization utilities."""

import re
from pathlib import Path
from typing import Dict, List, Optional

from .utils import get_logger

logger = get_logger(__name__)


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and lowercasing.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    # Convert to lowercase for consistency
    text = text.lower()
    
    return text


def extract_key_phrases(text: str, min_length: int = 3) -> List[str]:
    """Extract key phrases from text.
    
    Args:
        text: Input text
        min_length: Minimum length for phrases
        
    Returns:
        List of key phrases
    """
    if not text:
        return []
    
    # Split on common separators
    phrases = re.split(r'[,;.\n]', text)
    
    # Filter and normalize
    key_phrases = []
    for phrase in phrases:
        phrase = phrase.strip()
        if len(phrase) >= min_length:
            key_phrases.append(phrase)
    
    return key_phrases


def parse_document_metadata(filepath: Path) -> Dict[str, str]:
    """Parse basic metadata from a document path.
    
    Args:
        filepath: Path to the document
        
    Returns:
        Dictionary with metadata (name, extension, size)
    """
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return {}
    
    metadata = {
        "name": filepath.stem,
        "extension": filepath.suffix,
        "size_bytes": str(filepath.stat().st_size),
        "parent_dir": filepath.parent.name,
    }
    
    return metadata


def clean_field_name(field: str) -> str:
    """Clean a field name for use as a key.
    
    Args:
        field: Raw field name
        
    Returns:
        Cleaned field name
    """
    # Convert to lowercase
    field = field.lower()
    # Replace spaces and special chars with underscores
    field = re.sub(r'[^\w\s]', '', field)
    field = re.sub(r'\s+', '_', field)
    
    return field
