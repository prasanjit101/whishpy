import os
import json
from pathlib import Path
from typing import Optional, Tuple

class SettingsManager:
    """Handles all application settings and configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".whishpy"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir_exists()
        
    def _ensure_config_dir_exists(self):
        """Ensure the config directory exists"""
        self.config_dir.mkdir(exist_ok=True)
        
    def save_api_key(self, api_key: str, provider: str = "groq") -> None:
        """Save API key and provider to config file"""
        config = self._load_config()
        config.update({
            'api_key': api_key,
            'provider': provider
        })
        self._save_config(config)
        
    def load_api_key(self) -> Tuple[Optional[str], str]:
        """Load API key and provider from config file"""
        config = self._load_config()
        return config.get('api_key'), config.get('provider', 'groq')
        
    def save_max_recording_time(self, max_time: Optional[int]) -> None:
        """Save max recording time to config file"""
        config = self._load_config()
        config['max_recording_time'] = max_time
        self._save_config(config)
        
    def load_max_recording_time(self) -> Optional[int]:
        """Load max recording time from config file"""
        config = self._load_config()
        return config.get('max_recording_time')
        
    def _load_config(self) -> dict:
        """Load the config file or return empty dict if it doesn't exist"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
    def _save_config(self, config: dict) -> None:
        """Save the config file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
