"""
Configuration parser for Port Discord Bot.
Loads and parses config.yaml, expanding environment variables.
"""

import yaml
import os
from typing import Dict, Optional, Any


class ConfigParser:
    """
    Loads YAML configuration file and provides methods to access config values.
    Supports environment variable expansion via ${VAR_NAME} syntax.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize ConfigParser and load configuration.
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config = self._load_config(config_path)
        self.intents = self.config.get("intents", {})
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """
        Load YAML config and expand environment variables.
        
        Args:
            path: Path to config.yaml
        
        Returns:
            Parsed config dictionary with env vars expanded
        """
        # Load YAML file
        with open(path) as f:
            config = yaml.safe_load(f)
        
        # Expand ${VAR} syntax by converting to string, replacing, then re-parsing
        config_str = yaml.dump(config)
        for key, value in os.environ.items():
            config_str = config_str.replace(f"${{{key}}}", str(value))
        
        return yaml.safe_load(config_str)
    
    def parse_intent(self, message: str) -> Optional[str]:
        """
        Match message against configured keywords.
        
        Args:
            message: User's Discord message
        
        Returns:
            Intent name if matched, None otherwise
        """
        lower = message.lower().strip()
        
        for intent_name, intent_config in self.intents.items():
            keywords = intent_config.get("keywords", [])
            if any(kw in lower for kw in keywords):
                return intent_name
        
        return None
    
    def get_intent_config(self, intent_name: str) -> Dict[str, Any]:
        """
        Get full configuration for a specific intent.
        
        Args:
            intent_name: Name of intent (key in intents section)
        
        Returns:
            Intent configuration dictionary
        """
        return self.intents.get(intent_name, {})
    
    def get_api_token(self) -> str:
        """Get Port.io API token"""
        return self.config.get("port_api_token", "")
    
    def get_discord_token(self) -> str:
        """Get Discord bot token"""
        return self.config.get("discord_token", "")
    
    def get_discord_channel(self) -> str:
        """Get Discord channel name to listen on"""
        return self.config.get("discord_channel", "port-herp-ops")
