from dataclasses import dataclass, field

from models.database_config import DatabaseConfig
from models.server_config import ServerConfig

@dataclass
class AppConfig:
    Database: DatabaseConfig = field(default_factory=DatabaseConfig)
    Server: ServerConfig = field(default_factory=DatabaseConfig)