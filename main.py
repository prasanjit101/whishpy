#!/usr/bin/env python3
"""
Voice-to-Text Transcription Menubar App using Groq's API
This script creates a menu bar app that allows you to record audio,
transcribe it with Groq, and insert it at your cursor position.
"""

import os
import threading
import rumps
from src.audio_recorder import AudioRecorder
from src.transcription_service import TranscriptionService
from src.text_inserter import TextInserter
from src.circular_logger import logger, setup_logging

class VoiceToTextApp(rumps.App):
    def __init__(self):
        super(VoiceToTextApp, self).__init__("🎙️", quit_button=None)
        setup_logging()
        logger.info("Application initialized")
        
        # Load max recording time from config
        from src.config import load_max_recording_time
        self.max_recording_time = load_max_recording_time()
        
        # Initialize components
        self.audio_recorder = AudioRecorder(
            max_recording_time=self.max_recording_time,
            stop_callback=self._process_recording
        )
        self.transcription_service = TranscriptionService()
        self.text_inserter = TextInserter()
        
        # Setup menu
        self.click_to_record_item = rumps.MenuItem("Click to Start/Stop Recording", callback=self.toggle_recording)
        self.prompt_item = rumps.MenuItem("Ask AI", callback=self.prompt_ai_with_selected_text)
        self.menu = [
            self.click_to_record_item,
            None,  # Separator
            self.prompt_item,
            None,  # Separator
            {
                "Settings": [
                    rumps.MenuItem("Set Max Recording Time...", callback=self.set_max_recording_time),
                    rumps.MenuItem("Set API Key", callback=self.set_api_key),
                ]
            },
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        self.is_prompt_mode = False
    
    def set_api_key(self, _):
        """Handle settings window for API key management."""
        logger.info("Opening API key settings")
        self.transcription_service._prompt_for_api_key()

    def set_max_recording_time(self, _):
        """Set maximum recording time in minutes."""
        from src.config import save_max_recording_time
        
        window = rumps.Window(
            message="Enter max recording time in minutes (0 to disable):",
            default_text=str(self.max_recording_time // 60 if self.max_recording_time else ""),
            title="Set Max Recording Time",
            ok="Save",
            cancel="Cancel",
            dimensions=(200, 30)
        )
        
        response = window.run()
        if response.clicked:
            try:
                minutes = int(response.text)
                if minutes < 0:
                    raise ValueError("Time must be positive")
                
                if minutes == 0:
                    self.max_recording_time = None
                    save_max_recording_time(None)
                    rumps.notification("Max Recording Time", "Disabled", "Max recording time disabled")
                else:
                    self.max_recording_time = minutes * 60
                    save_max_recording_time(self.max_recording_time)
                    rumps.notification(
                        "Max Recording Time", 
                        "Set", 
                        f"Max recording time set to {minutes} minutes"
                    )
                    
                # Update AudioRecorder with new max time
                self.audio_recorder.max_recording_time = self.max_recording_time
                
            except ValueError as e:
                rumps.alert("Invalid Input", "Please enter a valid number of minutes")
    
    def quit_app(self, _):
        """Quit the application."""
        logger.info("Application shutdown initiated")
        # Ensure all resources are cleaned up
        if self.audio_recorder.is_recording:
            self.audio_recorder.stop_recording()
        rumps.quit_application()
    
    def toggle_recording(self, _):
        """Toggle between starting and stopping recording."""
        if self.is_prompt_mode:
            return
        if self.audio_recorder.is_recording:
            self._stop_recording()
        else:
            self.click_to_record_item.title = "Click to Stop Recording"
            self._start_recording()
    
    def _start_recording(self):
        """Start audio recording."""
        logger.info("Starting recording")
        if not self.audio_recorder.start_recording():
            error_msg = "Unable to start recording"
            logger.error(error_msg)
            rumps.alert("Recording Error", error_msg)
            return
        
        self.title = "🔴"
    
    def _stop_recording(self):
        """Stop audio recording and process the audio."""
        logger.info("Stopping recording")
        audio_file = self.audio_recorder.stop_recording()
        
        if not audio_file:
            error_msg = "No audio file was recorded"
            logger.error(error_msg)
            rumps.alert("Recording Error", error_msg)
            return
        
        self.title = "⏳"
        # Determine which processing function to use
        if self.is_prompt_mode:
            thread = threading.Thread(target=self._process_prompt_recording, args=(audio_file,))
        else:
            thread = threading.Thread(target=self._process_recording, args=(audio_file,))
        thread.daemon = True
        thread.start()
    
    def prompt_ai_with_selected_text(self, _):
        """Handle the Prompt menu item click."""
        if self.audio_recorder.is_recording:
            if self.is_prompt_mode: 
                self._stop_recording()
            else:
                return
        else:
            self.is_prompt_mode = True
            self.prompt_item.title = "Generating...Click to Stop"
            self._start_recording()
        
    
    def _process_prompt_recording(self, audio_file):
        """Process the recording for prompt functionality."""
        def process():
            try:
                logger.info(f"Processing prompt recording: {audio_file}")

                # Transcribe audio
                transcription = self.transcription_service.transcribe_audio(audio_file)
                if not transcription:
                    logger.warning("Empty transcription received")
                    return

                # Get selected text
                selected_text = self.text_inserter.get_selected_text()

                # Generate response
                response = self.transcription_service.generate_response_with_context(
                    transcription,
                    selected_text
                )

                # Show response
                # rumps.notification(
                #     "Whishpy Response",
                #     "Here's the response to your prompt:",
                #     response
                # )
                self.text_inserter.insert_text_with_shortcut(response)

            except ValueError as e:
                logger.error(f"Value Error processing prompt recording: {str(e)}")
                rumps.alert("Error", str(e))
            except OSError as e:
                logger.error(f"OS Error processing prompt recording: {str(e)}")
                rumps.alert("Error", str(e))
            except Exception as e:
                logger.error(f"General Error processing prompt recording: {str(e)}")
                rumps.alert("Error", str(e))
            finally:
                # Clean up temp file
                try:
                    os.unlink(audio_file)
                    logger.debug(f"Cleaned up temp file: {audio_file}")
                except Exception as e:
                    logger.error(f"Error cleaning up temp file: {str(e)}")

                # Reset UI
                self.title = "🎙️"
                self.prompt_item.title = "Prompt"
                self.click_to_record_item.title = "Click to Start Recording"
                self.is_prompt_mode = False

        # Run processing in background thread
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def _process_recording(self, audio_file):
        """Process the recorded audio file."""
        def process():
            try:
                logger.info(f"Processing recording: {audio_file}")
                # Transcribe audio
                transcription = self.transcription_service.transcribe_audio(audio_file)
                
                if transcription:
                    logger.info(f"Transcription successful: {transcription}")
                    # Only insert text if this is a regular recording
                    if not self.prompt_item.title == "Recording... Click to Stop":
                        self.text_inserter.insert_text_with_shortcut(transcription)
                else:
                    logger.warning("Empty transcription received")
            except Exception as e:
                logger.error(f"Error processing recording: {str(e)}")
                rumps.alert("Error", str(e))
            finally:
                # Clean up temp file
                try:
                    os.unlink(audio_file)
                    logger.debug(f"Cleaned up temp file: {audio_file}")
                except Exception as e:
                    logger.error(f"Error cleaning up temp file: {str(e)}")
                
                # Reset UI
                self.title = "🎙️"
                self.click_to_record_item.title = "Click to Start Recording"
        
        # Run processing in background thread
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    # Add support for clicking directly on the menu bar icon
    app = VoiceToTextApp()
    
    # Custom handle of icon click to toggle recording
    @rumps.clicked("icon")
    def icon_clicked(sender):
        app.toggle_recording(None)
    
    app.run()
