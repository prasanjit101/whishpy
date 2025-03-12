# Whishpy

a python script that can run inside of mac m1 os and transcribe my voice to text using open ai api and enter the text at my current pointer. 
I want to use the python script with mac's shortcuts or automations whichever is better

## Project Product Requirements Document (PRD)

**1. Introduction**

This document outlines the requirements for a macOS application that transcribes voice to text using the OpenAI Whisper API and inserts the transcribed text at the user's current cursor position. The application will be accessible through the macOS menu bar and offer flexible recording options.

**2. Goals**

* Provide a convenient and efficient way for users to transcribe voice to text on macOS.
* Enable seamless insertion of transcribed text into any application.
* Offer flexible recording options to cater to various user needs.
* Create a user-friendly application accessible from the menu bar.
* Provide a way to trigger the script automatically on login.

**3. Target Audience**

* Individuals who frequently need to transcribe voice to text.
* Users who prefer voice input over typing.
* Professionals who need to quickly capture notes or ideas.
* Anyone seeking a convenient voice-to-text solution on macOS.

**4. Functional Requirements**

* **Voice Recording:**
    * Capture audio from the user's microphone.
    * Offer timed recording options (5s, 10s, 15s, 30s, custom).
    * Implement click-to-start and click-to-stop recording functionality.
    * Real time audio capture during click to start/stop mode.
* **Transcription:**
    * Utilize the OpenAI Whisper API to transcribe recorded audio.
    * Handle background processing of audio to prevent system freezes.
* **Text Insertion:**
    * Copy the transcribed text to the clipboard.
    * Simulate keyboard presses to paste the text at the current cursor position.
* **Menu Bar Application:**
    * Display a microphone icon (🎙️) in the macOS menu bar.
    * Provide a menu with recording options and settings.
    * Display visual status indicators (🎙️ Ready, 🔴 Recording, ⏳ Processing).
    * Add a setting menu to configure the OpenAI API key.
* **Settings:**
    * Allow users to input and store their OpenAI API key.
* **Startup:**
    * Provide an option to automatically start the application on macOS login.
* **Standalone Application (Optional):**
    * Provide instructions to create a standalone macOS application using py2app.

**5. Non-Functional Requirements**

* **Performance:**
    * Ensure minimal latency between voice input and text output.
    * Efficient background processing to avoid system slowdowns.
* **Usability:**
    * Intuitive and easy-to-use interface.
    * Clear and concise instructions for setup and usage.
* **Reliability:**
    * Stable and consistent performance.
    * Robust error handling.
* **Security:**
    * Secure storage of the OpenAI API key.
* **Compatibility:**
    * Compatible with macOS M1 and later.

**6. User Interface (UI) Requirements**

* **Menu Bar Icon:**
    * Microphone icon (🎙️) to indicate the application's presence.
    * Status indicators:
        * 🎙️: Ready
        * 🔴: Recording
        * ⏳: Processing
* **Menu Items:**
    * Timed recording options (5s, 10s, 15s, 30s, Custom).
    * "Click to Start/Stop Recording" option.
    * Settings menu.
* **Settings Window:**
    * Text field for entering the OpenAI API key.

**7. Technical Requirements**

* **Programming Language:** Python
* **Libraries:**
    * PyAudio (for audio recording)
    * OpenAI Python library (for Whisper API)
    * rumps (for menu bar application)
    * py2app (Optional, for standalone application)
    * pyperclip (for clipboard access)
    * pynput (for keyboard simulation)
* **Operating System:** macOS M1 and later
* **API:** OpenAI Whisper API

**8. Setup and Installation**

* Provide clear and detailed setup instructions.
* Include instructions for installing required Python packages.
* Explain how to obtain and configure the OpenAI API key.
* Provide instructions for creating a macOS Shortcut or Automator workflow (if applicable).
* Provide instructions for adding the application to Login Items.
* Provide instructions to create a standalone application using py2app.

**9. Testing**

* Unit testing for individual components.
* Integration testing for end-to-end functionality.
* User acceptance testing (UAT) to ensure usability and reliability.

**10. Future Considerations**

* Support for multiple languages.
* Integration with other cloud services.
* Advanced settings for audio input and output.
* Adding a setting to choose the openai model.
* Adding a setting to choose the output language.
