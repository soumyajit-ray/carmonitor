"""
Configuration management for Car Monitor project.
Loads and validates configuration from YAML files.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the car monitor system."""
    
    def __init__(self, config_file: str = None, phase: int = 1):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file. If None, uses default for phase.
            phase: Phase number (1, 2, or 3)
        """
        self.phase = phase
        self.project_root = Path(__file__).parent.parent
        
        if config_file is None:
            config_file = self.project_root / f"config/phase{phase}_config.yaml"
        else:
            config_file = Path(config_file)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            self._config = yaml.safe_load(f)
        
        # Resolve relative paths
        self._resolve_paths()
    
    def _resolve_paths(self):
        """Convert relative paths in config to absolute paths."""
        if 'logging' in self._config and 'directory' in self._config['logging']:
            log_dir = self._config['logging']['directory']
            if not os.path.isabs(log_dir):
                self._config['logging']['directory'] = str(
                    self.project_root / log_dir
                )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'obd.port' or 'display.width')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config = Config()
            >>> port = config.get('obd.port')
            >>> width = config.get('display.width', 640)
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., 'obd', 'display')
            
        Returns:
            Dictionary with section configuration
        """
        return self._config.get(section, {})
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'obd.port')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, output_file: Optional[str] = None):
        """
        Save configuration to file.
        
        Args:
            output_file: Output file path. If None, overwrites original file.
        """
        if output_file is None:
            output_file = self.project_root / f"config/phase{self.phase}_config.yaml"
        
        with open(output_file, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    @property
    def obd_port(self) -> str:
        """Get OBD-II port."""
        return self.get('obd.port', '/dev/rfcomm0')
    
    @property
    def log_directory(self) -> str:
        """Get log directory path."""
        return self.get('logging.directory')
    
    @property
    def debug(self) -> bool:
        """Get debug mode status."""
        return self.get('system.debug', False)
    
    def __repr__(self) -> str:
        return f"Config(phase={self.phase}, config={self._config})"


# Global configuration instance (can be imported directly)
_global_config = None


def get_config(phase: int = 1) -> Config:
    """
    Get global configuration instance.
    
    Args:
        phase: Phase number (1, 2, or 3)
        
    Returns:
        Global Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(phase=phase)
    return _global_config
