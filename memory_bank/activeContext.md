**Current Focus:** Refactoring codebase for better maintainability and performance

**Recent Changes:**

* Created SettingsManager class for centralized configuration management
* Added LLM instance caching in TranscriptionService
* Improved type hints across the codebase
* Updated system patterns documentation
* Enhanced error handling and resource management
* Refactored configuration handling to use SettingsManager
* Added proper cleanup procedures for LLM instances

**Next Steps:**

* Update LLM class to fully support both OpenAI and Groq providers
* If text insertion fails, copy the text to the clipboard
* Add language support for other languages - Hindi, Spanish, French, Japanese
* Implemented prompt functionality in VoiceToTextApp, allowing users to generate responses based on selected text.
* Added max recording time feature with settings management and background processing
* Improved text insertion method by adding fallback to direct typing if paste shortcut fails.
* Implemented text insertion via Command+V shortcut for better user experience.
* Implemented logging functionality with a circular logger for better error tracking and application monitoring.
* Refactored API key management to load from a config file and save user input, enhancing security and usability.
* Added LLM class for response generation and refactor transcription service to utilize LLM for audio transcriptions, improving modularity and code organization.
* Enhanced LLM response generation with context.
* Fixed a bug in `src/llm.py` where the `context` parameter could be `None`, causing a `TypeError` during string concatenation. Added a check to ensure `context` is always a string.
* Updated UI elements for better user experience and maintainability.

**Active Decisions:**

* Using Groq Whisper for accurate transcription
* Implementing robust error handling and resource management
* Maintaining modular design for better maintainability
* Direct text insertion instead of clipboard
