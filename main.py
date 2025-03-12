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

class VoiceToTextApp(rumps.App):
    def __init__(self):
        super(VoiceToTextApp, self).__init__("🎙️", quit_button=None)
        
        # Initialize components
        self.audio_recorder = AudioRecorder()
        self.transcription_service = TranscriptionService()
        self.text_inserter = TextInserter()
        
        # Setup menu
        self.click_to_record_item = rumps.MenuItem("Click to Start/Stop Recording", callback=self.toggle_recording)
        self.menu = [
            self.click_to_record_item,
            None,  # Separator
            rumps.MenuItem("Settings", callback=self.settings),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
    
    def settings(self, _):
        """Handle settings window for API key management."""
        self.transcription_service._prompt_for_api_key()
    
    def quit_app(self, _):
        """Quit the application."""
        # Ensure all resources are cleaned up
        if self.audio_recorder.is_recording:
            self.audio_recorder.stop_recording()
        rumps.quit_application()
    
    def toggle_recording(self, _):
        """Toggle between starting and stopping recording."""
        if self.audio_recorder.is_recording:
            self._stop_recording()
        else:
            self._start_recording()
    
    def _start_recording(self):
        """Start audio recording."""
        if not self.audio_recorder.start_recording():
            rumps.alert("Recording Error", "Unable to start recording")
            return
        
        self.title = "🔴"
        self.click_to_record_item.title = "Click to Stop Recording"
    
    def _stop_recording(self):
        """Stop audio recording and process the audio."""
        audio_file = self.audio_recorder.stop_recording()
        
        if not audio_file:
            rumps.alert("Recording Error", "No audio file was recorded")
            return
        
        self.title = "⏳"
        
        # Process recording in background thread
        thread = threading.Thread(target=self._process_recording, args=(audio_file,))
        thread.daemon = True
        thread.start()
    
    def _process_recording(self, audio_file):
        """Process the recorded audio file."""
        try:
            # Transcribe audio
            transcription = self.transcription_service.transcribe_audio(audio_file)
            
            if transcription:
                # Insert text at cursor
                self.text_inserter.insert_text(transcription)
        except Exception as e:
            rumps.alert("Error", str(e))
        finally:
            # Clean up temp file
            try:
                os.unlink(audio_file)
            except:
                pass
            
            # Reset UI
            self.title = "🎙️"
            self.click_to_record_item.title = "Click to Start Recording"

if __name__ == "__main__":
    # Add support for clicking directly on the menu bar icon
    app = VoiceToTextApp()
    
    # Custom handle of icon click to toggle recording
    @rumps.clicked("icon")
    def icon_clicked(sender):
        app.toggle_recording(None)
    
    app.run()
