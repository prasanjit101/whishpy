import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".whishpy"
CONFIG_FILE = CONFIG_DIR / "config.json"

def save_api_key(api_key):
    """Save API key to config file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'api_key': api_key}, f)

def load_api_key():
    """Load API key from config file if it exists"""
    if not CONFIG_FILE.exists():
        return None
        
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        return config.get('api_key')
