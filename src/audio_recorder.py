import pyaudio
import wave
import tempfile
import time

class AudioRecorder:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.frames = []
        self.sample_rate = 44100
        self.chunk = 1024
        self.format_type = pyaudio.paInt16
        self.channels = 1
        self.is_recording = False
        self.start_time = 0

    def start_recording(self):
        """Start audio recording."""
        if self.is_recording:
            return False

        self.audio = pyaudio.PyAudio()
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
        return True

    def stop_recording(self):
        """Stop audio recording and return the recorded audio file path."""
        if not self.is_recording:
            return None

        # Updated duration check using captured frames
        duration = (len(self.frames) * self.chunk) / self.sample_rate
        if not self.frames or duration < 1.0:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.is_recording = False
            raise ValueError("Recording must be at least 1 second long")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_filename = temp_file.name
        temp_file.close()

        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format_type))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

        self.is_recording = False
        return temp_filename

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Audio stream callback to collect frames."""
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def get_recording_duration(self):
        """Get the duration of the current recording."""
        if not self.is_recording:
            return 0
        return time.time() - self.start_time
