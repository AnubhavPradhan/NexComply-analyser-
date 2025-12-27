"""Command-line interface for NexComply Analyser."""

import shutil
from pathlib import Path
from typing import Optional

import click

from nexcomply_analyser import __version__
from nexcomply_analyser.ingestion import DataIngestion
from nexcomply_analyser.risk_report import RiskReportGenerator
from nexcomply_analyser.utils import get_logger, get_project_root

logger = get_logger(__name__)


@click.group()
@click.version_option(version=__version__)
def cli():
    """NexComply Analyser - GRC Compliance Analysis Tool.

    This tool helps analyze compliance frameworks, questionnaires,
    and risk reports for GRC (Governance, Risk, and Compliance) activities.
    """
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def ingest(verbose: bool):
    """Read and process inputs from existing data folders.

    This command scans the following directories:
    - New Format Policy Docs
    - Questionnaires
    - Frameworks
    - Risk Reports
    - Dummy KL
    """
    if verbose:
        logger.setLevel("DEBUG")

    click.echo("Starting data ingestion...")

    try:
        ingestion = DataIngestion()
        data = ingestion.ingest_all()

        click.echo("\n=== Ingestion Summary ===")
        click.echo(f"Policy Documents: {len(data['policy_documents'])}")
        click.echo(f"Questionnaires: {len(data['questionnaires'])}")
        click.echo(f"Frameworks: {len(data['frameworks'])}")

        if verbose:
            click.echo("\n=== Policy Documents ===")
            for doc in data["policy_documents"]:
                click.echo(f"  - {doc['name']}")

            click.echo("\n=== Questionnaires ===")
            for q in data["questionnaires"]:
                click.echo(f"  - {q['name']}")

            click.echo("\n=== Frameworks ===")
            for f in data["frameworks"]:
                click.echo(f"  - {f['name']}")

        click.echo("\n✓ Ingestion complete!")

    except Exception as e:
        click.echo(f"✗ Error during ingestion: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--output-dir", "-o", default=None, help="Output directory for reports")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def analyze(output_dir: Optional[str], verbose: bool):
    """Produce a risk report from ingested data.

    This command analyzes the ingested data and generates:
    - CSV risk report
    - JSON risk report

    Reports are saved to the Risk Reports/ directory by default.
    """
    if verbose:
        logger.setLevel("DEBUG")

    click.echo("Starting risk analysis...")

    try:
        generator = RiskReportGenerator()

        # Override output directory if specified
        if output_dir:
            generator.output_dir = Path(output_dir)

        # Generate reports
        report_paths = generator.generate_reports()

        click.echo("\n=== Analysis Complete ===")
        click.echo(f"CSV Report: {report_paths['csv']}")
        click.echo(f"JSON Report: {report_paths['json']}")
        click.echo("\n✓ Reports generated successfully!")

    except Exception as e:
        click.echo(f"✗ Error during analysis: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--copy", is_flag=True, help="Copy notebooks to notebooks/ directory")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def notebooks(copy: bool, verbose: bool):
    """List and optionally organize Jupyter notebooks.

    This command finds all .ipynb files in the repository and can
    optionally copy them to a centralized notebooks/ directory.
    """
    if verbose:
        logger.setLevel("DEBUG")

    root = get_project_root()
    notebooks_dir = root / "notebooks"

    # Find all notebooks
    notebook_files = list(root.rglob("*.ipynb"))
    # Exclude notebooks already in the notebooks/ directory
    notebook_files = [nb for nb in notebook_files if not str(nb).startswith(str(notebooks_dir))]

    if not notebook_files:
        click.echo("No notebooks found in the repository.")
        return

    click.echo(f"Found {len(notebook_files)} notebook(s):\n")

    for nb in notebook_files:
        rel_path = nb.relative_to(root)
        click.echo(f"  - {rel_path}")

    if copy:
        click.echo(f"\nCopying notebooks to {notebooks_dir}...")
        notebooks_dir.mkdir(exist_ok=True)

        for nb in notebook_files:
            dest = notebooks_dir / nb.name

            # Handle name conflicts
            counter = 1
            while dest.exists():
                stem = nb.stem
                dest = notebooks_dir / f"{stem}_{counter}.ipynb"
                counter += 1

            shutil.copy2(nb, dest)
            click.echo(f"  ✓ Copied: {nb.name} -> {dest.name}")

        click.echo("\n✓ Notebooks copied successfully!")
    else:
        click.echo("\nUse --copy flag to copy notebooks to notebooks/ directory.")


@cli.command()
def info():
    """Display information about the NexComply Analyser environment."""
    click.echo(f"NexComply Analyser v{__version__}")
    click.echo(f"Project Root: {get_project_root()}")
    click.echo("\nData Directories:")

    data_dirs = [
        "New Format Policy Docs",
        "Questionnaires",
        "Frameworks",
        "Risk Reports",
        "Dummy KL",
        "Session on GRC",
    ]

    for dir_name in data_dirs:
        dir_path = get_project_root() / dir_name
        exists = "✓" if dir_path.exists() else "✗"
        click.echo(f"  {exists} {dir_name}")


if __name__ == "__main__":
    cli()
