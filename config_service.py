# config/config_service.py
from dataclasses import asdict
from typing import List, Dict, Any
from config_loader import ConfigLoader
from models.app_config import AppConfig, DatabaseConfig, ServerConfig

class ConfigService:
    def __init__(self, config_dir: str):
        self.config_loader = ConfigLoader(config_dir)

    def _load_and_transform_configs(self) -> List[AppConfig]:
        raw_configs = self.config_loader.load_configs()
        app_configs = []
        for config in raw_configs:
            database_config = DatabaseConfig(**config.get('Database', {}))
            server_config = ServerConfig(**config.get('Server', {}))
            app_config = AppConfig(Database=database_config, Server=server_config)
            app_configs.append(app_config)
        return app_configs

    def get_configs(self) -> List[AppConfig]:
        return self._load_and_transform_configs()

    def get_configs_as_dict(self) -> List[Dict[str, Any]]:
        return [asdict(config) for config in self.get_configs()]
