# Whishpy

a python script that can run inside of mac m1 os and transcribe my voice to text using open ai api and enter the text at my current pointer. 
I want to use the python script with mac's shortcuts or automations whichever is better

## Voice-to-Text Transcription Setup Guide

This guide provides instructions for both the command-line script and the menu bar application.

### Prerequisites

1. **Python 3.7+** (already installed on Mac M1)
2. **Groq API Key** - You'll need to [create an account](https://platform.groq.com/signup) and get an API key
3. **Required Python packages**

### Installation Steps

1. **Install the required packages:**

For the command-line script:
```bash
pip3 install pyaudio wave groq pyperclip pynput
```

For the menu bar application (includes all the above plus rumps):
```bash
pip3 install pyaudio wave groq pyperclip pynput rumps py2app
```

2. **Set up your Groq API key as an environment variable:**

```bash
echo 'export GROQ_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

3. **Save the Python script:**
   - Save the provided script to a location of your choice (e.g., `~/scripts/whish.py`)
   - Make it executable: `chmod +x ~/scripts/whish.py`

### Setting Up with macOS Shortcuts (Recommended)

1. **Open the Shortcuts app** on your Mac

2. **Create a new shortcut:**
   - Click the "+" button to create a new shortcut
   - Name it something like "Voice to Text"

3. **Add a "Run Shell Script" action:**
   - Search for "Run Shell Script" in the actions panel and add it
   - Set the shell to `/bin/zsh`
   - Enter the following command:
     ```bash
     /usr/bin/python3 /path/to/your/whish.py --duration 5
     ```
   - Adjust the duration as needed (default is 5 seconds)

4. **Add a keyboard shortcut:**
   - Click on the ⓘ icon in the top right corner of the shortcut
   - Click "Add Keyboard Shortcut"
   - Choose a keyboard combination (e.g., Option+Command+T)

### Setting Up with Automator (Alternative)

1. **Open Automator** and create a new Quick Action

2. **Configure the workflow:**
   - Set "Workflow receives" to "no input" in "any application"

3. **Add a "Run Shell Script" action:**
   - Search for and add the "Run Shell Script" action
   - Set the shell to `/bin/zsh`
   - Enter the following command:
     ```bash
     /usr/bin/python3 /path/to/your/whish.py --duration 5
     ```

4. **Save the workflow** with a descriptive name like "Voice to Text"

5. **Add a keyboard shortcut:**
   - Open System Settings > Keyboard > Keyboard Shortcuts
   - Select "Services" in the left panel
   - Find your "Voice to Text" service and assign a keyboard shortcut

### Usage

1. Place your cursor where you want the transcribed text to appear
2. Trigger the shortcut (using the keyboard shortcut you assigned)
3. Speak clearly for the duration set (default is 5 seconds)
4. Wait a moment for the audio to be processed and transcribed
5. The transcribed text will be automatically pasted at your cursor position

### Menu Bar Application Setup

1. **Save the menubar app script:**
   - Save the provided menu bar script to a location of your choice (e.g., `~/scripts/whish.py`)
   - Make it executable: `chmod +x ~/scripts/whish.py`

2. **Run the app:**
   ```bash
   python3 ~/scripts/whish.py
   ```

3. **Setting up to start automatically:**
   - Open System Settings > General > Login Items
   - Click the "+" button
   - Navigate to your script and add it

4. **Building a standalone app (optional):**
   
   Create a file named `setup.py` in the same directory as your script:
   ```python
   from setuptools import setup

   APP = ['whish.py']
   DATA_FILES = []
   OPTIONS = {
       'argv_emulation': True,
       'plist': {
           'LSUIElement': True,
       },
       'packages': ['rumps', 'pyaudio', 'groq', 'pyperclip', 'pynput'],
   }

   setup(
       app=APP,
       data_files=DATA_FILES,
       options={'py2app': OPTIONS},
       setup_requires=['py2app'],
   )
   ```

   Then build the app:
   ```bash
   python3 setup.py py2app
   ```

   This will create a standalone app in the `dist` folder that you can move to your Applications folder.

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