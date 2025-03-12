from pynput.keyboard import Key, Controller
import time

class TextInserter:
    def __init__(self):
        self.keyboard = Controller()

    def insert_text(self, text):
        """Insert text at current cursor position."""
        if not text:
            return

        # Simulate typing the text
        for char in text:
            self.keyboard.type(char)
            time.sleep(0.01)  # Small delay for reliability

    def insert_text_with_shortcut(self, text):
        """Insert text using Command+V shortcut."""
        if not text:
            return

        # Simulate Command+V (paste)
        with self.keyboard.pressed(Key.cmd):
            self.keyboard.press('v')
            self.keyboard.release('v')
