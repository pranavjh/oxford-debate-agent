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

# Load environment variables (optional, API key loaded from config/secrets/config.json)
load_dotenv()

app = typer.Typer(
    help="🎭 Oxford Debate Agent - Generate AI-powered debates with audio output",
    add_completion=False
)
console = Console()


def check_config():
    """Verify that API configuration exists."""
    config_path = Path("config/secrets/config.json")
    if not config_path.exists():
        console.print("[bold red]Error:[/bold red] API configuration not found!")
        console.print(f"\nPlease copy your OpenAI config.json to: [yellow]{config_path}[/yellow]")
        console.print("\nThe file should contain your OpenAI API key:")
        console.print("  {")
        console.print('    "OPENAI_API_KEY": "sk-...",')
        console.print('    "OPENAI_API_BASE": "https://api.openai.com/v1/"')
        console.print("  }")
        raise typer.Exit(1)


@app.command()
def generate(
    motion: str = typer.Argument(
        ...,
        help="The debate motion"
    ),
    output_dir: str = typer.Option(
        "output",
        "--output",
        "-o",
        help="Output directory for audio files"
    ),
    config_path: str = typer.Option(
        "config/config.yaml",
        "--config",
        "-c",
        help="Path to configuration file"
    ),
):
    """
    Generate an Oxford-style debate with audio output.

    Examples:\n
        python src/main.py generate "AI will benefit humanity"\n
        python src/main.py generate "Trump's tariffs help the US economy" -o debates/\n
    """

    console.print("\n[bold cyan]🎭 Oxford Debate Agent[/bold cyan]\n")

    # Check for API configuration
    check_config()

    console.print(f"[yellow]Motion:[/yellow] {motion}\n")

    # Initialize orchestrator (will load API key from config/secrets/config.json)
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
def examples():
    """List example debate motions."""
    console.print("\n[bold cyan]📋 Example Debate Motions:[/bold cyan]\n")

    motions = [
        "This house believes that artificial intelligence will do more good than harm",
        "This house believes that social media does more harm than good",
        "This house would ban autonomous weapons systems",
        "This house believes that privacy is dead in the digital age",
        "This house would prioritize economic growth over environmental protection",
        "This house believes that universal basic income is necessary",
        "This house would ban genetic engineering of humans",
        "This house believes that space exploration is a waste of resources",
        "Trump's tariffs are helping the US economy",
        "Remote work is better than office work",
    ]

    for i, motion in enumerate(motions, 1):
        console.print(f"  {i}. [cyan]{motion}[/cyan]")

    console.print("\n[dim]Use any of these with:[/dim]")
    console.print('  [dim]python src/main.py generate "your motion here"[/dim]\n')


if __name__ == "__main__":
    app()
