"""Tests for parsing utilities."""

import pytest

from nexcomply_analyser.parsing import (
    clean_field_name,
    extract_key_phrases,
    normalize_text,
)


def test_normalize_text():
    """Test text normalization."""
    # Test with extra whitespace
    text = "  Hello   World  "
    result = normalize_text(text)
    assert result == "hello world"
    
    # Test with newlines
    text = "Hello\n\nWorld"
    result = normalize_text(text)
    assert result == "hello world"
    
    # Test empty string
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_extract_key_phrases():
    """Test key phrase extraction."""
    text = "Security policy, access control; data privacy. Compliance"
    phrases = extract_key_phrases(text)
    
    assert len(phrases) > 0
    assert any("security" in p.lower() for p in phrases)
    
    # Test with short phrases filtered out
    text = "a, b, Security Policy"
    phrases = extract_key_phrases(text, min_length=3)
    assert all(len(p) >= 3 for p in phrases)
    
    # Test empty input
    assert extract_key_phrases("") == []
    assert extract_key_phrases(None) == []


def test_clean_field_name():
    """Test field name cleaning."""
    # Test with spaces and special characters
    field = "User Name (Full)"
    result = clean_field_name(field)
    assert result == "user_name_full"
    
    # Test with multiple spaces
    field = "First   Last"
    result = clean_field_name(field)
    assert result == "first_last"
    
    # Test with uppercase
    field = "EMAIL_ADDRESS"
    result = clean_field_name(field)
    assert result == "email_address"


def test_normalize_text_preserves_single_spaces():
    """Test that single spaces are preserved."""
    text = "one two three"
    result = normalize_text(text)
    assert result == "one two three"


def test_extract_key_phrases_respects_min_length():
    """Test that min_length parameter works."""
    text = "a, bb, ccc, dddd"
    phrases = extract_key_phrases(text, min_length=4)
    assert all(len(p) >= 4 for p in phrases)
