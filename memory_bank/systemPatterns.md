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

**Provider Selection Flow:**

1. User selects "Set API Key" from menu
2. Application shows API key input and provider selection
3. User enters API key and selects provider (OpenAI or Groq)
4. Configuration saved to ~/.whishpy/config.json
5. TranscriptionService loads provider and API key on initialization
6. LLM instance created with selected provider and API key

**Component Relationships:**

* Menu bar -> AudioRecorder -> TranscriptionService -> TextInserter
