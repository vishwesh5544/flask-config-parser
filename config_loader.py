import configparser
import os
from typing import Any, Dict, List, Optional

import yaml

from models.app_config import AppConfig
from models.database_config import DatabaseConfig
from models.server_config import ServerConfig


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

    def load_configs(self) -> List[AppConfig]:
        configs = []
        for filename in os.listdir(self.config_dir):
            file_path = os.path.join(self.config_dir, filename)
            if filename.endswith('.yaml'):
                file_data = self._load_yaml(file_path)
            elif filename.endswith('.ini'):
                file_data = self._load_ini(file_path)
            else:
                continue

            # Use reflection to map dict to data classes
            database_config = DatabaseConfig(**file_data.get('Database', {}))
            server_config = ServerConfig(**file_data.get('Server', {}))
            app_config = AppConfig(Database=database_config, Server=server_config)
            configs.append(app_config)

        return configs
    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def _load_ini(self, file_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}

    def _compare_configs(self, config1: Dict[str, Any], config2: Dict[str, Any]) -> bool:
        return config1 == config2

    def _merge_configs(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        if not base:
            return updates
        if self._compare_configs(base, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in base:
                    base[key] = self._merge_configs(base[key], value)
                else:
                    base[key] = value
        return base

    def load_config(self) -> Optional[AppConfig]:
        config_data = {}
        for filename in os.listdir(self.config_dir):
            file_path = os.path.join(self.config_dir, filename)
            if filename.endswith('.yaml'):
                file_data = self._load_yaml(file_path)
            elif filename.endswith('.ini'):
                file_data = self._load_ini(file_path)
            else:
                continue

            if not config_data:
                config_data = file_data
            else:
                config_data = self._merge_configs(config_data, file_data)

        if not config_data:
            return None

        # Use reflection to map dict to data classes
        database_config = DatabaseConfig(**config_data.get('Database', {}))
        server_config = ServerConfig(**config_data.get('Server', {}))
        app_config = AppConfig(Database=database_config, Server=server_config)

        return app_config