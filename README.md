# Whishpy

A free and open-source Wispr flow Alternative

## Demo

[A demo of Whishpy](https://youtu.be/-CVD5dJUDyU)

## Voice-to-Text Transcription Setup Guide

This guide provides instructions for both the command-line script and the menu bar application.

### Usage

1. Place your cursor where you want the transcribed text to appear
2. Trigger the shortcut (using the keyboard shortcut you assigned)
3. Speak clearly for the duration set (default is 5 seconds)
4. Wait a moment for the audio to be processed and transcribed
5. The transcribed text will be automatically pasted at your cursor position
6. You can also press the 'ask AI' button to get assistance from an AI.
7. Highlight the text you want to get assistance with and press the 'ask AI' button to manipulate the highlighted text.

### Automated Installation Steps

1. **Install the required packages:**

```bash
./setup.sh
```

2. **Run the app:**
move the dist/Whishpy.app to your Applications folder

3. **Run the app:**
open the app and it will ask you to allow microphone access. Add it to login items. Add the required accessibility permissions

4. **Use the app:**
click the microphone icon in the menu bar and start recording or click on "ask ai" to talk to an AI assistant.

For more information on how to use the app, see the [setup.md](setup.md) file.



### Usage

1. Place your cursor where you want the transcribed text to appear
2. Trigger the shortcut (using the keyboard shortcut you assigned)
3. Speak clearly for the duration set (default is 5 seconds)
4. Wait a moment for the audio to be processed and transcribed
5. The transcribed text will be automatically pasted at your cursor position
6. You can also press the 'ask AI' button to get assistance from an AI.
7. Highlight the text you want to get assistance with and press the 'ask AI' button to manipulate the highlighted text.


### Using the Menu Bar App

1. Click on the microphone icon (🎙️) in the menu bar
2. Select one of the preset recording durations or choose "Custom Duration..."
3. Speak for the selected duration
4. The app will transcribe your speech and paste it at your current cursor position
5. The icon will change to indicate status:
   - 🎙️ - Ready
   - 🔴 - Recording
   - ⏳ - Processing
6. You can also press the 'ask AI' button to get assistance from an AI.
7. Highlight the text you want to get assistance with and press the 'ask AI' button to manipulate the highlighted text.

#### Click-to-Start/Stop Recording
1. Click directly on the microphone icon in the menu bar to start recording
2. Click again when you're done to stop recording and start transcription
3. Alternatively, use the "Start transcribing" menu item

### Troubleshooting

- **Microphone permissions**: Make sure to grant microphone access to Terminal/Shortcuts/Your app when prompted
- **API key issues**: Verify your Groq API key is correctly set in the environment or through the app settings
- **PyAudio installation problems**: If you encounter issues installing PyAudio, try:
  ```bash
  brew install portaudio
  pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
  ```
- **Menu bar app not showing**: Some Mac screens (especially those with notches) can hide menu bar items. Try clicking in the menu bar area where the app should be.
