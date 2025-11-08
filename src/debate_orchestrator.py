"""
Debate Orchestrator

Coordinates the flow of the Oxford debate, managing agents and state.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

import yaml
from langchain_openai import ChatOpenAI


class DebateOrchestrator:
    """Orchestrates the Oxford-style debate flow."""

    def __init__(self, motion: str, config_path: str = "config/config.yaml", output_dir: str = "output"):
        """
        Initialize the debate orchestrator.

        Args:
            motion: The debate motion
            config_path: Path to configuration file
            output_dir: Directory for output files
        """
        self.motion = motion
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load OpenAI API key from secrets
        self._load_api_key()

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Load prompts
        with open('config/prompts.yaml', 'r') as f:
            self.prompts = yaml.safe_load(f)

        # Initialize LLM with latest model
        self.llm = ChatOpenAI(
            model=self.config['agents']['proposition']['model'],
            temperature=self.config['agents']['proposition']['temperature']
        )

        # Debate state
        self.debate_content: Dict[str, str] = {}

    def _load_api_key(self):
        """Load OpenAI API key from config/secrets/config.json."""
        secrets_path = Path("config/secrets/config.json")

        if not secrets_path.exists():
            raise FileNotFoundError(
                f"API key configuration not found at {secrets_path}. "
                "Please copy your OpenAI config.json to config/secrets/config.json"
            )

        with open(secrets_path, 'r') as f:
            secrets = json.load(f)

        # Set API key in environment (supports multiple key formats)
        api_key = secrets.get('OPENAI_API_KEY') or secrets.get('openai_api_key') or secrets.get('API_KEY')

        if not api_key:
            raise ValueError("No OpenAI API key found in config/secrets/config.json")

        os.environ['OPENAI_API_KEY'] = api_key

        # Optionally set API base URL if specified
        api_base = secrets.get('OPENAI_API_BASE') or secrets.get('openai_api_base')
        if api_base:
            os.environ['OPENAI_API_BASE'] = api_base

    def generate_debate(self) -> Dict[str, str]:
        """
        Generate the complete debate content.

        Returns:
            Dictionary mapping stage to generated text
        """
        # 1. Generate opening statements
        self.debate_content['proposition_opening'] = self._generate_speech(
            'proposition_opening',
            {}
        )

        self.debate_content['opposition_opening'] = self._generate_speech(
            'opposition_opening',
            {}
        )

        # 2. Generate rebuttals
        self.debate_content['proposition_rebuttal'] = self._generate_speech(
            'proposition_rebuttal',
            {'opposition_opening': self.debate_content['opposition_opening']}
        )

        self.debate_content['opposition_rebuttal'] = self._generate_speech(
            'opposition_rebuttal',
            {'proposition_opening': self.debate_content['proposition_opening']}
        )

        # 3. Generate closing statements
        self.debate_content['proposition_closing'] = self._generate_speech(
            'proposition_closing',
            {
                'proposition_opening': self.debate_content['proposition_opening'],
                'opposition_opening': self.debate_content['opposition_opening'],
                'proposition_rebuttal': self.debate_content['proposition_rebuttal'],
                'opposition_rebuttal': self.debate_content['opposition_rebuttal'],
            }
        )

        self.debate_content['opposition_closing'] = self._generate_speech(
            'opposition_closing',
            {
                'proposition_opening': self.debate_content['proposition_opening'],
                'opposition_opening': self.debate_content['opposition_opening'],
                'proposition_rebuttal': self.debate_content['proposition_rebuttal'],
                'opposition_rebuttal': self.debate_content['opposition_rebuttal'],
            }
        )

        return self.debate_content

    def _generate_speech(self, stage: str, context: Dict[str, str]) -> str:
        """
        Generate a speech for a specific stage.

        Args:
            stage: The debate stage (e.g., 'proposition_opening')
            context: Previous speeches for context

        Returns:
            Generated speech text
        """
        # Get prompt template
        prompt_template = self.prompts['system_prompts'][stage]

        # Format with motion and context
        prompt = prompt_template.format(
            motion=self.motion,
            **context
        )

        # Generate speech
        response = self.llm.invoke(prompt)
        return response.content

    def generate_audio(self, debate_content: Dict[str, str]) -> List[str]:
        """
        Generate audio files from debate content.

        Args:
            debate_content: Dictionary of stage -> text

        Returns:
            List of generated audio file paths
        """
        from audio_generator import AudioGenerator

        audio_gen = AudioGenerator(self.config)

        audio_files = []

        # Define order and metadata
        speech_order = [
            ('proposition_opening', 'proposition', 'opening', 1),
            ('opposition_opening', 'opposition', 'opening', 2),
            ('proposition_rebuttal', 'proposition', 'rebuttal', 3),
            ('opposition_rebuttal', 'opposition', 'rebuttal', 4),
            ('proposition_closing', 'proposition', 'closing', 5),
            ('opposition_closing', 'opposition', 'closing', 6),
        ]

        for stage, side, stage_name, order in speech_order:
            text = debate_content[stage]

            # Generate filename
            filename = self.config['output']['filename_pattern'].format(
                order=order,
                side=side,
                stage=stage_name
            )
            output_path = self.output_dir / filename

            # Generate audio
            audio_gen.text_to_speech(
                text=text,
                output_path=str(output_path),
                voice=side
            )

            audio_files.append(str(output_path))

            # Optionally save transcript
            if self.config['output']['metadata']['include_transcript']:
                transcript_path = output_path.with_suffix('.txt')
                with open(transcript_path, 'w') as f:
                    f.write(f"# {side.upper()} - {stage_name.upper()}\\n\\n")
                    f.write(f"Motion: {self.motion}\\n\\n")
                    f.write(text)

        return audio_files
