import os
import rumps
from src.llm import LLM
import time
from typing import Optional
from .config import save_api_key, load_api_key
from src.circular_logger import logger, setup_logging

class TranscriptionService:
    def __init__(self):
        self.api_key = None
        self.provider = 'groq'
        self._load_api_key()
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        setup_logging()

    def _load_api_key(self):
        """Load API key and provider from config file or prompt user."""
        self.api_key, self.provider = load_api_key()
        if not self.api_key:
            self._prompt_for_api_key()

    def _prompt_for_api_key(self):
        """Prompt user for API key and provider, then save to config."""
        api_key, _ = load_api_key()
        
        # Create window with provider selection buttons
        provider_window = rumps.Window(
            "Please select your provider:",
            "Provider Setup",
            default_text="",
            ok="Select one from below",
            dimensions=(0, 0)
        )
        provider_window.add_button("OpenAI")
        provider_window.add_button("Groq")
        
        # Show provider selection window
        provider_response = provider_window.run()
        logger.info(f"Provider response: {provider_response}")
        if not provider_response.clicked:
            return
            
        # Update provider based on button clicked
        selected_provider = provider_response.clicked
        if selected_provider == 1:
            logger.info("None selected")
            return
        elif selected_provider == 2:
            self.provider = "openai"
        elif selected_provider == 3:
            self.provider = "groq"
        else:
            logger.error(f"Unknown provider selected: {selected_provider}")
            return
        
        # Create window for API key input
        key_window = rumps.Window(
            "Please enter your API Key:",
            "API Key Setup", 
            default_text=api_key if api_key else "",
            dimensions=(300, 50)
        )

        # Show API key input window
        key_response = key_window.run()
        if not key_response.clicked or not key_response.text:
            return
            
        # Save API key and provider
        self.api_key = key_response.text
        logger.info(f"API key: {self.api_key}, Provider: {self.provider}")
        save_api_key(self.api_key, self.provider)

    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using Groq's Whisper API with retry logic."""
        if not self.api_key:
            raise ValueError("API key is not set")

        llm = LLM(self.api_key, self.provider)
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                with open(audio_file_path, "rb") as audio_file:
                    try:
                        response = llm.groq.audio.transcriptions.create(
                            file=(audio_file_path, audio_file.read()),
                            model="whisper-large-v3-turbo",
                            language="en",
                            timeout=10  # 10 second timeout
                        )
                    except Exception as e:
                        print(f"Transcription attempt {attempt + 1} failed: {e}")
                        raise
                return response.text
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                continue
        raise Exception(f"Transcription failed after {self.max_retries} attempts: {str(last_error)}")

    def generate_response_with_context(self, prompt: str, context: str) -> str:
        """Generate a response from the LLM with the given prompt and context."""
        if not self.api_key:
            raise ValueError("API key is not set")
        
        llm = LLM(self.api_key)
        try:
            response = llm.generate_response(prompt, context)
            return response
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
