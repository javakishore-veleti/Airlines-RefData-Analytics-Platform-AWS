"""Environment-based config for MasterData-API."""

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
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_vhost: str
    rabbitmq_queue: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            mysql_host=os.environ.get("ARFD_MYSQL_HOST", "127.0.0.1"),
            mysql_port=int(os.environ.get("ARFD_MYSQL_PORT", "3306")),
            mysql_user=os.environ.get("ARFD_MYSQL_USER", "arfd"),
            mysql_password=os.environ.get("ARFD_MYSQL_PASSWORD", "arfd"),
            mysql_database=os.environ.get("ARFD_MYSQL_DATABASE", "market_db"),
            api_host=os.environ.get("ARFD_API_HOST", "127.0.0.1"),
            api_port=int(os.environ.get("ARFD_API_PORT", "8110")),
            rabbitmq_host=os.environ.get("ARFD_RABBITMQ_HOST", "127.0.0.1"),
            rabbitmq_port=int(os.environ.get("ARFD_RABBITMQ_PORT", "5672")),
            rabbitmq_user=os.environ.get("ARFD_RABBITMQ_USER", "arfd"),
            rabbitmq_password=os.environ.get("ARFD_RABBITMQ_PASSWORD", "arfd"),
            rabbitmq_vhost=os.environ.get("ARFD_RABBITMQ_VHOST", "arfd"),
            rabbitmq_queue=os.environ.get("ARFD_RABBITMQ_QUEUE", "arfd.masterdata.events"),
        )


def get_settings() -> Settings:
    return Settings.from_env()
