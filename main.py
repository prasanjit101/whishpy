#!/usr/bin/env python3
"""
Voice-to-Text Transcription Menubar App using Groq's API
This script creates a menu bar app that allows you to record audio,
transcribe it with Groq, and paste it at your cursor position.
"""

import os
import tempfile
import time
import subprocess
import json
import threading
import rumps
import pyaudio
import wave
import openai
import pyperclip
from pynput.keyboard import Key, Controller
from groq import Groq

# Initialize keyboard controller for simulating key presses
keyboard = Controller()

# Default recording duration
DEFAULT_DURATION = 5

class VoiceToTextApp(rumps.App):
    def __init__(self):
        super(VoiceToTextApp, self).__init__("🎙️", quit_button=None)
        
        # Setup menu
        self.click_to_record_item = rumps.MenuItem("Click to Start/Stop Recording", callback=self.toggle_recording)
        self.menu = [
            self.click_to_record_item,
            None,  # Separator
            rumps.MenuItem("Settings", callback=self.settings),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        # Get API key from environment or settings
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            self.api_key = rumps.Window(
                "Please enter your Groq API Key:",
                "API Key Setup",
                default_text="",
                dimensions=(300, 20)
            ).run().text
            # Save API key (in a real app, you'd store this securely)
            if self.api_key:
                os.environ["GROQ_API_KEY"] = self.api_key
        
        # Status variables
        self.is_recording = False
        self.is_processing = False
        self.manual_recording = False
        self.recording_stream = None
        self.audio = None
        self.frames = []
        self.manual_start_time = 0
        self.sample_rate = 44100
        self.chunk = 1024
        self.format_type = pyaudio.paInt16
        self.channels = 1
    
    def custom_duration(self, _):
        response = rumps.Window(
            "Enter recording duration in seconds:",
            "Custom Duration",
            default_text="5",
            dimensions=(100, 20)
        ).run()
        
        if response.clicked:
            try:
                duration = int(response.text)
                if duration > 0:
                    self.start_transcription(duration)
                else:
                    rumps.alert("Invalid duration", "Please enter a positive number.")
            except ValueError:
                rumps.alert("Invalid input", "Please enter a valid number.")
    
    def settings(self, _):
        # Create a simple settings window
        response = rumps.Window(
            "Groq API Key:",
            "Settings",
            default_text=self.api_key or "",
            dimensions=(300, 20),
            ok="Save",
            cancel="Cancel"
        ).run()
        
        if response.clicked:
            self.api_key = response.text
            os.environ["GROQ_API_KEY"] = self.api_key
    
    def quit_app(self, _):
        rumps.quit_application()
    
    def toggle_recording(self, _):
        """Toggle between starting and stopping manual recording."""
        # Check if we're currently doing a timed recording
        if self.is_recording and not self.manual_recording:
            rumps.alert("Recording in progress", "A timed recording is already in progress.")
            return
            
        # Check if we're currently processing
        if self.is_processing:
            rumps.alert("Processing in progress", "Please wait for the current operation to complete.")
            return
            
        if not self.api_key:
            rumps.alert("API Key Missing", "Please set your Groq API key in the Settings.")
            return
            
        if not self.manual_recording:
            # Start recording
            self.start_manual_recording()
        else:
            # Stop recording and process
            self.stop_manual_recording()
    
    def start_manual_recording(self):
        """Start manual recording mode."""
        self.manual_recording = True
        self.is_recording = True
        self.title = "🔴"
        self.click_to_record_item.title = "Click to Stop Recording"
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Reset frames
        self.frames = []
        
        # Start recording
        self.recording_stream = self.audio.open(
            format=self.format_type,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.audio_callback
        )
        
        self.manual_start_time = time.time()
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream to collect frames."""
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def stop_manual_recording(self):
        """Stop manual recording and start processing."""
        if not self.manual_recording:
            return
            
        # Stop recording
        duration = time.time() - self.manual_start_time
        
        if self.recording_stream:
            self.recording_stream.stop_stream()
            self.recording_stream.close()
            self.recording_stream = None
        
        if self.audio:
            self.audio.terminate()
            self.audio = None
        
        self.manual_recording = False
        
        # Update UI
        self.click_to_record_item.title = "Click to Start/Stop Recording"
        
        # If recording was too short, alert and don't process
        if duration < 1.0:
            self.is_recording = False
            self.title = "🎙️"
            rumps.alert("Recording too short", "Recording must be at least 1 second long.")
            return
            
        # Save audio to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_filename = temp_file.name
        temp_file.close()
        
        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format_type))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        
        # Process the recording
        self.is_processing = True
        self.title = "⏳"
        
        # Create and start a thread for transcription
        thread = threading.Thread(target=self.process_manual_recording, args=(temp_filename,))
        thread.daemon = True
        thread.start()
    
    def process_manual_recording(self, audio_file_path):
        """Process a manually recorded audio file."""
        try:
            # Transcribe audio
            transcription = self.transcribe_audio(audio_file_path)
            
            # Paste text at cursor
            if transcription:
                self.paste_text_at_cursor(transcription)
            
            # Clean up the temporary audio file
            try:
                os.unlink(audio_file_path)
            except:
                pass
                
        except Exception as e:
            rumps.alert("Error", str(e))
            
        finally:
            # Reset status
            self.is_recording = False
            self.is_processing = False
            self.title = "🎙️"
    
    def start_transcription(self, duration):
        """Start the transcription process in a separate thread."""
        if self.is_recording or self.is_processing:
            rumps.alert("Already in progress", "Please wait for the current operation to complete.")
            return
        
        if not self.api_key:
            rumps.alert("API Key Missing", "Please set your Groq API key in the Settings.")
            return
        
        # Update title to show status
        self.title = "🔴"
        self.is_recording = True
        
        # Create and start a new thread for the recording and transcription
        thread = threading.Thread(target=self.transcribe_workflow, args=(duration,))
        thread.daemon = True
        thread.start()
    
    def transcribe_workflow(self, duration):
        """Handle the full transcription workflow."""
        try:
            # Record audio
            audio_file_path = self.record_audio(duration)
            
            # Update status
            self.is_recording = False
            self.is_processing = True
            self.title = "⏳"
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_file_path)
            
            # Paste text at cursor
            if transcription:
                self.paste_text_at_cursor(transcription)
            
            # Clean up the temporary audio file
            try:
                os.unlink(audio_file_path)
            except:
                pass
            
        except Exception as e:
            rumps.alert("Error", str(e))
        
        finally:
            # Reset status
            self.is_recording = False
            self.is_processing = False
            self.title = "🎙️"

    def record_audio(self, duration=5, sample_rate=44100, channels=1, format_type=pyaudio.paInt16):
        """Record audio for the specified duration and save to a temporary file."""
        # Create a temporary file to store the audio
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_filename = temp_file.name
        temp_file.close()
        
        # Set up PyAudio
        chunk = 1024
        audio = pyaudio.PyAudio()
        
        # Open audio stream for recording
        stream = audio.open(format=format_type,
                          channels=channels,
                          rate=sample_rate,
                          input=True,
                          frames_per_buffer=chunk)
        
        frames = []
        for _ in range(0, int(sample_rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the audio to the temporary file
        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format_type))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        
        return temp_filename

    def transcribe_audio(self, audio_file_path):
        """Transcribe audio using Groq's Whisper API."""
        groq = Groq(api_key=self.api_key)
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = groq.audio.transcriptions.create(
                    file=(audio_file_path, audio_file.read()), # Required audio file
                    model="whisper-large-v3-turbo", # Required model to use for transcription
                    language="en",  # Optional
                )
            
            transcription = response.text
            return transcription
        except Exception as e:
            rumps.alert("Transcription Error", str(e))
            return None

    def paste_text_at_cursor(self, text):
        """Copy text to clipboard and simulate paste command at current cursor position."""
        if not text:
            return
        
        # Copy text to clipboard
        pyperclip.copy(text)
        
        # Simulate Command+V (paste)
        with keyboard.pressed(Key.cmd):
            keyboard.press('v')
            keyboard.release('v')

if __name__ == "__main__":
    # Add support for clicking directly on the menu bar icon
    app = VoiceToTextApp()
    
    # Custom handle of icon click to toggle recording
    @rumps.clicked("icon")
    def icon_clicked(sender):
        app.toggle_recording(None)
    
    app.run()