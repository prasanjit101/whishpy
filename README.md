# Whishpy

a python script that can run inside of mac m1 os and transcribe my voice to text using open ai api and enter the text at my current pointer. 
I want to use the python script with mac's shortcuts or automations whichever is better

## Voice-to-Text Transcription Setup Guide

This guide provides instructions for both the command-line script and the menu bar application.

### Prerequisites

1. **Python 3.7+** (already installed on Mac M1)
2. **Groq API Key** - You'll need to [create an account](https://platform.groq.com/signup) and get an API key

### Automated Installation Steps

1. **Install the required packages:**

```bash
./build_app.sh
```

2. **Run the app:**
move the dist/Whishpy.app to your Applications folder

3. **Run the app:**
open the app and it will ask you to allow microphone access

4. **Use the app:**
click the microphone icon in the menu bar and start recording

For more information on how to use the app, see the [setup.md](setup.md) file.


### Using the Menu Bar App

1. Click on the microphone icon (🎙️) in the menu bar
2. Select one of the preset recording durations or choose "Custom Duration..."
3. Speak for the selected duration
4. The app will transcribe your speech and paste it at your current cursor position
5. The icon will change to indicate status:
   - 🎙️ - Ready
   - 🔴 - Recording
   - ⏳ - Processing

#### Click-to-Start/Stop Recording
1. Click directly on the microphone icon in the menu bar to start recording
2. Click again when you're done to stop recording and start transcription
3. Alternatively, use the "Click to Start/Stop Recording" menu item

### Troubleshooting

- **Microphone permissions**: Make sure to grant microphone access to Terminal/Shortcuts/Your app when prompted
- **API key issues**: Verify your Groq API key is correctly set in the environment or through the app settings
- **PyAudio installation problems**: If you encounter issues installing PyAudio, try:
  ```bash
  brew install portaudio
  pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
  ```
- **Menu bar app not showing**: Some Mac screens (especially those with notches) can hide menu bar items. Try clicking in the menu bar area where the app should be.