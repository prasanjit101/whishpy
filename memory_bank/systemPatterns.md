**Architecture:**

* Menu bar application (rumps) as the primary interface
* Modular components:
  - AudioRecorder: Handles audio capture using PyAudio
  - TranscriptionService: Manages Groq API communication
  - TextInserter: Handles text insertion using pynput

**Technical Decisions:**

* Python for cross-platform compatibility
* Groq Whisper for accurate transcription
* Modular design for better maintainability
* Direct text insertion instead of clipboard usage

**Design Patterns:**

* Event-driven (menu actions)
* Asynchronous processing (API calls)
* Single Responsibility Principle (separate classes for different concerns)
* Enhanced error handling and resource management
  - Proper cleanup of audio resources
  - API error handling and retries
  - Resource cleanup on application exit
* LLM integration for response generation
* Improved text insertion method with fallback to direct typing
* UI updates for better user experience and maintainability

**Component Relationships:**

* Menu bar -> AudioRecorder -> TranscriptionService -> TextInserter
