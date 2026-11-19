from __future__ import annotations
from typing import Protocol
import pymysql
from app.config import Settings, get_settings

class HealthDao(Protocol):
    def ping(self) -> bool: ...

class MysqlHealthDao:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
    def ping(self) -> bool:
        s = self._settings
        conn = pymysql.connect(host=s.mysql_host, port=s.mysql_port, user=s.mysql_user,
                               password=s.mysql_password, database=s.mysql_database,
                               charset="utf8mb4", connect_timeout=3)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1"); cur.fetchone()
            return True
        finally:
            conn.close()
