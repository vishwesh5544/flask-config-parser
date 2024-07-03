from dataclasses import asdict
from typing import Any, Dict
from config_loader import ConfigLoader
from models.app_config import AppConfig


class ConfigService:
    _instance = None

    def __new__(cls, config_dir: str):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
            cls._instance._initialize(config_dir)
        return cls._instance

    def _initialize(self, config_dir: str):
        self.config_loader = ConfigLoader(config_dir)
        self.config = self.config_loader.load_config()

    def get_config(self) -> AppConfig:
        return self.config

    def get_config_as_dict(self) -> Dict[str, Any]:
        return asdict(self.config)