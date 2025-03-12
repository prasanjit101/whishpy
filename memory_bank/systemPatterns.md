**Architecture:**

* Menu bar application (rumps) as the primary interface.
* PyAudio for audio capture.
* OpenAI API for transcription.
* pyperclip for clipboard access.
* pynput for keyboard simulation.

**Technical Decisions:**

* Python for cross-platform compatibility.
* OpenAI Whisper for accurate transcription.
* Streaming audio for click to start/stop.

**Design Patterns:**

* Event-driven (menu actions).
* Asynchronous processing (API calls).

**Component Relationships:**

* Menu bar -> Audio capture -> API call -> Text insertion.
