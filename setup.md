## Installation

### Automated Installation Steps

1. **Install the required packages:**

```bash
./setup.sh
```

2. **Run the app:**
move the dist/Whishpy.app to your Applications folder

3. **Run the app:**
open the app. Allow microphone access and add it to login items

4. **Use the app:**
click the microphone icon in the menu bar and start recording or press the 'ask AI' button to get assistance from an AI.



### Manual Installation Steps

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
     /usr/bin/python3 /path/to/your/whish.py
     ```

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
     /usr/bin/python3 /path/to/your/whish.py
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
6. You can also press the 'ask AI' button to get assistance from an AI.
7. Highlight the text you want to get assistance with and press the 'ask AI' button to manipulate the highlighted text.

### Menu Bar Application Setup

1. **Save the menubar app script:**
   - Make `./setup.sh` executable: `chmod +x setup.sh`
   - Run the script (e.g., `./setup.sh`) to create the `whish.py` script - 
      It will make the script executable and save it to `~/scripts/whish.py`

2. **Run the app:**
   ```bash
   python3 ~/scripts/whish.py
   ```

3. **Setting up to start automatically:**
   - Open System Settings > General > Login Items
   - Click the "+" button
   - Navigate to your script and add it
