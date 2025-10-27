import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


class OpenAITTS:
    """Generate speech audio using OpenAI's text-to-speech models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "tts-1",
        default_voice: str = "alloy",
        output_format: str = "mp3",
    ) -> None:
        self.client = OpenAI(api_key=api_key if api_key else os.environ.get('OPENAI_API_KEY'))
        self.model = model
        self.default_voice = default_voice
        self.output_format = output_format

    def generate_audio(self, text: str, voice: Optional[str] = None, output_path: str = "output.mp3") -> Path:
        """Generate speech audio for ``text`` and save it to ``output_path``.

        The OpenAI SDK has evolved quickly, and the previous implementation relied
        on a ``response.content`` attribute that is no longer provided.  To keep
        the method working across SDK versions we first try to use the modern
        streaming helper (``with_streaming_response``).  If that is unavailable we
        gracefully fall back to the basic ``create`` method and extract raw bytes
        from the response.
        """

        resolved_path = Path(output_path)
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        selected_voice = voice or self.default_voice

        try:
            streaming = self.client.audio.speech.with_streaming_response
        except AttributeError:
            streaming = None

        if streaming is not None:
            with streaming.create(
                model=self.model,
                voice=selected_voice,
                input=text,
                response_format=self.output_format,
            ) as response:
                response.stream_to_file(resolved_path)
            return resolved_path

        # Fall back to non-streaming request.
        response = self.client.audio.speech.create(
            model=self.model,
            voice=selected_voice,
            input=text,
            response_format=self.output_format,
        )

        audio_bytes = getattr(response, "content", None)
        if audio_bytes is None:
            audio_bytes = getattr(response, "audio", None)
        if isinstance(audio_bytes, bytes):
            resolved_path.write_bytes(audio_bytes)
            return resolved_path

        raise RuntimeError("OpenAI audio response does not contain raw audio bytes")


# Example Usage
#tts = OpenAITTS(api_key="api_key")
# tts.generate_audio("Today is a wonderful day to build something people love!", voice="echo", output_path="today.mp3")

#tts.generate_audio("Esta es una prueba en español, a ver cómo se escucha.", voice="echo", output_path="spanish_today.mp3")
