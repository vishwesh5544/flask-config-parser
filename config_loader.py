import configparser
import os
from typing import Any, Dict

import yaml

from models.app_config import AppConfig
from models.database_config import DatabaseConfig
from models.server_config import ServerConfig


class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def _load_ini(self, file_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(file_path)
        return {section: dict(config.items(section)) for section in config.sections()}

    def _merge_configs(
        self, base: Dict[str, Any], updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        for key, value in updates.items():
            if isinstance(value, dict) and key in base:
                base[key] = self._merge_configs(base[key], value)
            else:
                base[key] = value
        return base

    def load_config(self) -> AppConfig:
        config_data = {}
        for filename in os.listdir(self.config_dir):
            file_path = os.path.join(self.config_dir, filename)
            if filename.endswith(".yaml"):
                file_data = self._load_yaml(file_path)
            elif filename.endswith(".ini"):
                file_data = self._load_ini(file_path)
            else:
                continue
            config_data = self._merge_configs(config_data, file_data)

        # Use reflection to map dict to data classes
        database_config = DatabaseConfig(**config_data.get("Database", {}))
        server_config = ServerConfig(**config_data.get("Server", {}))
        app_config = AppConfig(Database=database_config, Server=server_config)

        return app_config
