from dataclasses import dataclass

@dataclass
class DatabaseConfig: 
    host: str = ''
    port: int = 0
    username: str = ''
    password: str = ''