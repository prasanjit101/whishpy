import pyaudio
import wave
import tempfile
import time
import threading
from src.circular_logger import logger, setup_logging

class AudioRecorder:
    def __init__(self, max_recording_time=None, stop_callback=None):
        self.audio = None
        self.stream = None
        self.frames = []
        self.sample_rate = 44100
        self.chunk = 1024
        self.format_type = pyaudio.paInt16
        self.channels = 1
        self.is_recording = False
        self.start_time = 0
        self.max_recording_time = max_recording_time
        self.stop_callback = stop_callback
        self._lock = threading.Lock()
        self._initialize_audio()
        setup_logging()

    def _initialize_audio(self):
        """Initialize PyAudio instance if not already initialized."""
        if self.audio is None:
            try:
                self.audio = pyaudio.PyAudio()
            except Exception as e:
                print(f"Failed to initialize PyAudio: {str(e)}")
                self.audio = None
                return False
        return True

    def __del__(self):
        """Clean up resources when object is deleted."""
        self._cleanup()

    def _cleanup(self):
        """Internal method to clean up resources."""
        try:
            if self.stream and self.stream.is_active():
                self.stream.stop_stream()
                self.stream.close()
        except Exception as e:
            print(f"Stream cleanup error: {str(e)}")
        finally:
            self.stream = None

    def start_recording(self):
        """Start audio recording."""
        if self.is_recording or not self._initialize_audio():
            return False

        try:
            self.frames = []
            self.stream = self.audio.open(
                format=self.format_type,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self.audio_callback
            )
            self.is_recording = True
            self.start_time = time.time()
            
            if self.max_recording_time is not None:
                def timer():
                    logger.info(f"Starting timer with max_recording_time: {self.max_recording_time} seconds")
                    start_time = time.time()
                    time.sleep(self.max_recording_time)
                    elapsed = time.time() - start_time
                    logger.info(f"Timer completed after {elapsed:.2f} seconds")
                    with self._lock:
                        if self.is_recording:
                            audio_file = self.stop_recording()
                            if self.stop_callback and audio_file:
                                self.stop_callback(audio_file)
                
                timer_thread = threading.Thread(target=timer)
                timer_thread.daemon = True
                timer_thread.start()
                
            return True
        except Exception as e:
            print(f"Start recording error: {str(e)}")
            self._cleanup()
            return False

    def stop_recording(self):
        """Stop audio recording and return the recorded audio file path."""
        if not self.is_recording:
            return None

        try:
            # Updated duration check using captured frames
            duration = (len(self.frames) * self.chunk) / self.sample_rate
            if not self.frames or duration < 1.0:
                self._cleanup()
                self.is_recording = False
                raise ValueError("Recording must be at least 1 second long")

            # Save to temp file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_filename = temp_file.name
            temp_file.close()

            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format_type))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))

            return temp_filename
        except Exception as e:
            print(f"Stop recording error: {str(e)}")
            return None
        finally:
            self._cleanup()
            self.is_recording = False

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Audio stream callback to collect frames."""
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def get_recording_duration(self):
        """Get the duration of the current recording."""
        if not self.is_recording:
            return 0
        return time.time() - self.start_time
