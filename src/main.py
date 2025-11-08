#!/usr/bin/env python3
"""
Oxford Debate Agent - Main Entry Point

Generates a complete Oxford-style debate with audio output.
"""

import os
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from debate_orchestrator import DebateOrchestrator

# Load environment variables
load_dotenv()

app = typer.Typer()
console = Console()


@app.command()
def generate_debate(
    motion: Optional[str] = typer.Option(
        None,
        "--motion",
        "-m",
        help="The debate motion (e.g., 'AI will replace human creativity')"
    ),
    output_dir: Optional[str] = typer.Option(
        "output",
        "--output",
        "-o",
        help="Output directory for audio files"
    ),
    config_path: Optional[str] = typer.Option(
        "config/config.yaml",
        "--config",
        "-c",
        help="Path to configuration file"
    ),
):
    """
    Generate an Oxford-style debate with audio output.

    Example:
        python main.py --motion "AI will benefit humanity more than harm it"
    """

    console.print("\n[bold cyan]🎭 Oxford Debate Agent[/bold cyan]\n")

    # Use default motion if not provided
    if not motion:
        motion = os.getenv("DEFAULT_MOTION", "This house believes that artificial intelligence will do more good than harm")

    console.print(f"[yellow]Motion:[/yellow] {motion}\n")

    # Initialize orchestrator
    try:
        orchestrator = DebateOrchestrator(
            motion=motion,
            config_path=config_path,
            output_dir=output_dir
        )
    except Exception as e:
        console.print(f"[bold red]Error initializing orchestrator:[/bold red] {e}")
        raise typer.Exit(1)

    # Generate debate
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("[cyan]Generating debate...", total=None)

        try:
            debate_content = orchestrator.generate_debate()
            progress.update(task, description="[green]✓ Debate content generated")

            progress.update(task, description="[cyan]Generating audio files...")
            audio_files = orchestrator.generate_audio(debate_content)
            progress.update(task, description="[green]✓ Audio files generated")

        except Exception as e:
            console.print(f"\n[bold red]Error during generation:[/bold red] {e}")
            raise typer.Exit(1)

    # Display results
    console.print("\n[bold green]✓ Debate generation complete![/bold green]\n")
    console.print("[yellow]Generated files:[/yellow]")
    for i, file_path in enumerate(audio_files, 1):
        console.print(f"  {i}. {file_path}")

    console.print(f"\n[dim]Output directory: {output_dir}[/dim]\n")


@app.command()
def list_motions():
    """List example debate motions."""
    console.print("\n[bold cyan]Example Debate Motions:[/bold cyan]\n")

    motions = [
        "This house believes that artificial intelligence will do more good than harm",
        "This house believes that social media does more harm than good",
        "This house would ban autonomous weapons systems",
        "This house believes that privacy is dead in the digital age",
        "This house would prioritize economic growth over environmental protection",
        "This house believes that universal basic income is necessary",
        "This house would ban genetic engineering of humans",
        "This house believes that space exploration is a waste of resources",
    ]

    for i, motion in enumerate(motions, 1):
        console.print(f"  {i}. {motion}")

    console.print()


if __name__ == "__main__":
    app()
