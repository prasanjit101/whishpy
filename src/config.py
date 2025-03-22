from .settings_manager import SettingsManager

settings_manager = SettingsManager()

def save_api_key(api_key, provider="groq"):
    """Save API key and provider to config file"""
    settings_manager.save_api_key(api_key, provider)

def load_api_key():
    """Load API key and provider from config file if it exists"""
    return settings_manager.load_api_key()

def save_max_recording_time(max_time):
    """Save max recording time to config file"""
    settings_manager.save_max_recording_time(max_time)

def load_max_recording_time():
    """Load max recording time from config file if it exists"""
    return settings_manager.load_max_recording_time()
