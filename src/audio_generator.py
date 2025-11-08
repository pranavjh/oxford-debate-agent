"""
Audio Generator

Handles text-to-speech conversion using OpenAI TTS or ElevenLabs.
"""

import os
from pathlib import Path
from typing import Dict

from openai import OpenAI


class AudioGenerator:
    """Generates audio from text using TTS APIs."""

    def __init__(self, config: Dict):
        """
        Initialize the audio generator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.tts_provider = os.getenv('TTS_PROVIDER', 'openai')

        if self.tts_provider == 'openai':
            self.client = OpenAI()
        elif self.tts_provider == 'elevenlabs':
            try:
                from elevenlabs import generate, set_api_key
                set_api_key(os.getenv('ELEVENLABS_API_KEY'))
                self.elevenlabs_generate = generate
            except ImportError:
                raise ImportError("ElevenLabs SDK not installed. Run: pip install elevenlabs")

    def text_to_speech(
        self,
        text: str,
        output_path: str,
        voice: str = 'proposition'
    ) -> str:
        """
        Convert text to speech and save as audio file.

        Args:
            text: The text to convert
            output_path: Path to save the audio file
            voice: Voice identifier ('proposition' or 'opposition')

        Returns:
            Path to the generated audio file
        """
        if self.tts_provider == 'openai':
            return self._openai_tts(text, output_path, voice)
        elif self.tts_provider == 'elevenlabs':
            return self._elevenlabs_tts(text, output_path, voice)
        else:
            raise ValueError(f"Unsupported TTS provider: {self.tts_provider}")

    def _openai_tts(self, text: str, output_path: str, voice: str) -> str:
        """Generate audio using OpenAI TTS."""

        # Get voice configuration
        voice_config = self.config['audio']['voices'][voice]
        voice_id = voice_config['voice_id']
        speed = voice_config.get('speed', 1.0)

        # Generate audio
        response = self.client.audio.speech.create(
            model="tts-1-hd",  # or tts-1 for faster/cheaper
            voice=voice_id,
            input=text,
            speed=speed
        )

        # Save to file
        response.stream_to_file(output_path)

        return output_path

    def _elevenlabs_tts(self, text: str, output_path: str, voice: str) -> str:
        """Generate audio using ElevenLabs."""

        # Get voice configuration
        voice_config = self.config['audio']['voices'][voice]
        voice_id = voice_config['voice_id']

        # Generate audio
        audio = self.elevenlabs_generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )

        # Save to file
        with open(output_path, 'wb') as f:
            f.write(audio)

        return output_path

    def normalize_audio(self, audio_path: str) -> str:
        """
        Normalize audio levels (optional post-processing).

        Args:
            audio_path: Path to audio file

        Returns:
            Path to normalized audio file
        """
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize

            # Load audio
            audio = AudioSegment.from_file(audio_path)

            # Normalize
            normalized_audio = normalize(audio)

            # Save
            normalized_audio.export(audio_path, format='mp3')

            return audio_path

        except ImportError:
            # If pydub not available, skip normalization
            return audio_path
