import os
import rumps
from groq import Groq
import time
from typing import Optional

class TranscriptionService:
    def __init__(self):
        self.api_key = None
        self._load_api_key()
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def _load_api_key(self):
        """Load API key from environment or prompt user."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            self._prompt_for_api_key()

    def _prompt_for_api_key(self):
        """Prompt user for API key."""
        response = rumps.Window(
            "Please enter your Groq API Key:",
            "API Key Setup",
            default_text="",
            dimensions=(300, 20)
        ).run()
        
        if response.clicked and response.text:
            self.api_key = response.text
            os.environ["GROQ_API_KEY"] = self.api_key

    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using Groq's Whisper API with retry logic."""
        if not self.api_key:
            raise ValueError("API key is not set")

        groq = Groq(api_key=self.api_key)
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                with open(audio_file_path, "rb") as audio_file:
                    response = groq.audio.transcriptions.create(
                        file=(audio_file_path, audio_file.read()),
                        model="whisper-large-v3-turbo",
                        language="en",
                        timeout=10  # 10 second timeout
                    )
                return response.text
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue
        
        raise Exception(f"Transcription failed after {self.max_retries} attempts: {str(last_error)}")
