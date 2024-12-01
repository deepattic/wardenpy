from dataclasses import dataclass


@dataclass
class AppConfig:
    EXPORT_DIRECTORY: str = "data/"
    PASSWORD_LENGTH: int = 20
