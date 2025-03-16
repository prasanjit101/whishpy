
**Technologies:**

* Python 3.x
* PyAudio
* Groq Python library (using Groq Whisper for transcription)
* rumps
* pynput
* py2app (optional)
* LLM libraries

**File Structure:**

* main.py - Main application entry point
* src/ - Source code directory
  - audio_recorder.py - Handles audio recording
  - transcription_service.py - Manages API communication
  - text_inserter.py - Handles text insertion
  - llm.py - Handles LLM integration
  - __init__.py - Package initialization
* marketing/ - Contains marketing materials

**Development Setup:**

* macOS M1 or later
* Virtual environment for dependencies
* API key (Groq or OpenAI)
* Python packages: rumps, pyaudio, groq, pynput, openai

**Technical Constraints:**

* macOS specific menu bar implementation
* API key dependency (Groq or OpenAI)
* Provider selection support
* Audio permissions
* Direct text insertion requires accessibility permissions
* Improved API key loading with error handling for missing config file.
* Implemented logging functionality with a circular logger for better error tracking and application monitoring.
* Refactored setup script to copy application files to a dedicated 'whish' directory and ensure main script is executable

**Dependencies:**

* Python packages listed above
* Groq API or OpenAI API
