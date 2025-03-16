import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".whishpy"
CONFIG_FILE = CONFIG_DIR / "config.json"

def save_api_key(api_key, provider="groq"):
    """Save API key and provider to config file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'api_key': api_key, 'provider': provider}, f)

def load_api_key():
    """Load API key and provider from config file if it exists"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('api_key'), config.get('provider', 'groq')
    except FileNotFoundError:
        return None, 'groq'

def save_max_recording_time(max_time):
    """Save max recording time to config file"""
    CONFIG_DIR.mkdir(exist_ok=True)
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}
    
    config['max_recording_time'] = max_time
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_max_recording_time():
    """Load max recording time from config file if it exists"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('max_recording_time')
    except FileNotFoundError:
        return None
