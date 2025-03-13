from pynput.keyboard import Key, Controller
import time
from .circular_logger import logger
import pyperclip

class TextInserter:
    def __init__(self):
        self.keyboard = Controller()
        self.logger = logger

    def insert_text(self, text):
        """Insert text at current cursor position."""
        if not text:
            logger.warning("Empty text received")
            return

        # Simulate typing the text
        for char in text:
            self.keyboard.type(char)
            time.sleep(0.01)  # Small delay for reliability

    def insert_text_with_shortcut(self, text):
        """Insert text using Command+V shortcut with fallback to direct typing."""
        if not text:
            self.logger.warning("Empty text received for shortcut insertion")
            return
        
        try:
            # Copy the text to the clipboard
            pyperclip.copy(text)
            logger.info(f"Text copied to clipboard: {text}")
            
            # Try paste shortcut first
            try:
                with self.keyboard.pressed(Key.cmd):
                    self.keyboard.press('v')
                    self.keyboard.release('v')
                logger.info("Paste shortcut executed successfully")
            except Exception as e:
                logger.warning(f"Paste shortcut failed: {str(e)}. Falling back to direct typing")
                self.insert_text(text)
                
        except Exception as e:
            logger.error(f"Failed to insert text: {str(e)}")
            raise