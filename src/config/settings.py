"""
Settings Module

Centralized configuration management for S3 cost optimization.
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path


class Settings:
    """
    Application settings manager.
    
    Provides reusable configuration management with support for
    environment variables, config files, and default values.
    """
    
    DEFAULT_CONFIG = {
        'aws': {
            'region': 'us-east-1',
            'profile': None
        },
        'lifecycle': {
            'standard_ia_days': 30,
            'glacier_days': 90,
            'deep_archive_days': 180,
            'expiration_days': 365
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'monitoring': {
            'enabled': True,
            'interval_hours': 24
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings.
        
        Args:
            config_file: Path to JSON configuration file
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
        
        self.load_from_env()
    
    def load_from_file(self, config_file: str):
        """
        Load configuration from JSON file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self._merge_config(file_config)
        except Exception as e:
            raise ValueError(f"Failed to load config file: {str(e)}")
    
    def load_from_env(self):
        """
        Load configuration from environment variables.
        
        Environment variables override file configuration.
        """
        # AWS settings
        if os.getenv('AWS_REGION'):
            self.config['aws']['region'] = os.getenv('AWS_REGION')
        if os.getenv('AWS_PROFILE'):
            self.config['aws']['profile'] = os.getenv('AWS_PROFILE')
        
        # Lifecycle settings
        if os.getenv('STANDARD_IA_DAYS'):
            self.config['lifecycle']['standard_ia_days'] = int(os.getenv('STANDARD_IA_DAYS'))
        if os.getenv('GLACIER_DAYS'):
            self.config['lifecycle']['glacier_days'] = int(os.getenv('GLACIER_DAYS'))
        if os.getenv('EXPIRATION_DAYS'):
            self.config['lifecycle']['expiration_days'] = int(os.getenv('EXPIRATION_DAYS'))
        
        # Logging settings
        if os.getenv('LOG_LEVEL'):
            self.config['logging']['level'] = os.getenv('LOG_LEVEL')
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """
        Merge new configuration with existing configuration.
        
        Args:
            new_config: New configuration dictionary
        """
        for key, value in new_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'aws.region')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
    
    def save_to_file(self, config_file: str):
        """
        Save configuration to JSON file.
        
        Args:
            config_file: Path to save configuration
        """
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to save config file: {str(e)}")
