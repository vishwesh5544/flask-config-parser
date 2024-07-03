# config/config_loader.py
import os
import yaml
import configparser
from typing import Dict, Any, List

class ConfigLoader:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def _load_ini(self, file_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}

    def _normalize_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        # Convert all values to the appropriate types
        if 'Database' in config_data:
            config_data['Database']['port'] = int(config_data['Database']['port'])
        if 'Server' in config_data:
            config_data['Server']['port'] = int(config_data['Server']['port'])
        return config_data

    def _compare_configs(self, config1: Dict[str, Any], config2: Dict[str, Any]) -> bool:
        return config1 == config2

    def load_configs(self) -> List[Dict[str, Any]]:
        loaded_configs = []
        unique_configs = []

        for filename in os.listdir(self.config_dir):
            file_path = os.path.join(self.config_dir, filename)
            if filename.endswith('.yaml'):
                file_data = self._load_yaml(file_path)
            elif filename.endswith('.ini'):
                file_data = self._load_ini(file_path)
            else:
                continue

            # Normalize the configuration data
            normalized_data = self._normalize_config(file_data)
            loaded_configs.append(normalized_data)

        # Merge identical configs
        for config in loaded_configs:
            if not any(self._compare_configs(config, unique) for unique in unique_configs):
                unique_configs.append(config)

        return unique_configs
