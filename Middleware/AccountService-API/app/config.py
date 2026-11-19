from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str
    api_host: str
    api_port: int

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            mysql_host=os.environ.get("ARFD_MYSQL_HOST", "127.0.0.1"),
            mysql_port=int(os.environ.get("ARFD_MYSQL_PORT", "3306")),
            mysql_user=os.environ.get("ARFD_MYSQL_USER", "arfd"),
            mysql_password=os.environ.get("ARFD_MYSQL_PASSWORD", "arfd"),
            mysql_database=os.environ.get("ARFD_ACCOUNT_DATABASE", os.environ.get("ARFD_MYSQL_DATABASE", "market_db")),
            api_host=os.environ.get("ARFD_ACCOUNT_API_HOST", "127.0.0.1"),
            api_port=int(os.environ.get("ARFD_ACCOUNT_API_PORT", "8111")),
        )

def get_settings() -> Settings:
    return Settings.from_env()
