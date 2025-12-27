"""Tests for CLI commands."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from scripts.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test that CLI help works."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'NexComply Analyser' in result.output


def test_cli_version(runner):
    """Test that version command works."""
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


def test_info_command(runner):
    """Test info command."""
    result = runner.invoke(cli, ['info'])
    assert result.exit_code == 0
    assert 'NexComply Analyser' in result.output
    assert 'Project Root' in result.output


def test_ingest_command(runner):
    """Test ingest command."""
    result = runner.invoke(cli, ['ingest'])
    assert result.exit_code == 0
    assert 'Ingestion Summary' in result.output


def test_ingest_verbose(runner):
    """Test ingest command with verbose flag."""
    result = runner.invoke(cli, ['ingest', '--verbose'])
    assert result.exit_code == 0
    assert 'Ingestion Summary' in result.output


def test_analyze_command(runner):
    """Test analyze command creates output files."""
    result = runner.invoke(cli, ['analyze'])
    assert result.exit_code == 0
    assert 'Analysis Complete' in result.output
    assert 'CSV Report' in result.output
    assert 'JSON Report' in result.output


def test_analyze_with_custom_output(runner):
    """Test analyze command with custom output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ['analyze', '--output-dir', tmpdir])
        assert result.exit_code == 0
        
        # Check that files were created
        output_path = Path(tmpdir)
        csv_files = list(output_path.glob('*.csv'))
        json_files = list(output_path.glob('*.json'))
        
        assert len(csv_files) > 0, "CSV report should be created"
        assert len(json_files) > 0, "JSON report should be created"


def test_notebooks_command(runner):
    """Test notebooks command."""
    result = runner.invoke(cli, ['notebooks'])
    assert result.exit_code == 0
    # Output varies based on whether notebooks exist
    assert 'notebook' in result.output.lower()


def test_notebooks_copy(runner):
    """Test notebooks command with copy flag."""
    result = runner.invoke(cli, ['notebooks', '--copy'])
    assert result.exit_code == 0
