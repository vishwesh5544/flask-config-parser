from dataclasses import dataclass

@dataclass
class ServerConfig:
    address: str = ''
    port: int = 0