"""User persistence with salted PBKDF2 hashes; ensures schema + default seed."""

from __future__ import annotations

import hashlib
import os
import secrets
from typing import Any, Protocol

import pymysql

from app.config import Settings, get_settings

DEFAULT_USERNAME = "arfd-admin"
DEFAULT_PASSWORD = "arfd-admin"
DEFAULT_DISPLAY = "ARFD Admin"


def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return salt.hex(), digest.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    _, digest = _hash_password(password, salt=salt)
    return secrets.compare_digest(digest, hash_hex)


class UserDao(Protocol):
    def ensure_schema_and_seed(self) -> None: ...
    def list_users(self) -> list[dict[str, Any]]: ...
    def get_by_username(self, username: str) -> dict[str, Any] | None: ...
    def get_by_id(self, user_id: int) -> dict[str, Any] | None: ...
    def create(self, username: str, password: str, display_name: str, role: str) -> int: ...
    def update(self, user_id: int, display_name: str, role: str, password: str | None) -> bool: ...
    def delete(self, user_id: int) -> bool: ...


class MysqlUserDao:
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def _conn(self):
        s = self._settings
        return pymysql.connect(
            host=s.mysql_host,
            port=s.mysql_port,
            user=s.mysql_user,
            password=s.mysql_password,
            database=s.mysql_database,
            charset="utf8mb4",
            autocommit=False,
        )

    def ensure_schema_and_seed(self) -> None:
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS account_user (
                      user_id INT AUTO_INCREMENT PRIMARY KEY,
                      username VARCHAR(64) NOT NULL UNIQUE,
                      password_salt VARCHAR(64) NOT NULL,
                      password_hash VARCHAR(128) NOT NULL,
                      display_name VARCHAR(128) NOT NULL,
                      role VARCHAR(32) NOT NULL DEFAULT 'operator',
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                cur.execute("SELECT user_id FROM account_user WHERE username=%s", (DEFAULT_USERNAME,))
                if cur.fetchone() is None:
                    salt, digest = _hash_password(DEFAULT_PASSWORD)
                    cur.execute(
                        """
                        INSERT INTO account_user (username, password_salt, password_hash, display_name, role)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (DEFAULT_USERNAME, salt, digest, DEFAULT_DISPLAY, "admin"),
                    )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def list_users(self) -> list[dict[str, Any]]:
        self.ensure_schema_and_seed()
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, display_name, role FROM account_user ORDER BY user_id"
                )
                cols = [d[0] for d in cur.description]
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        finally:
            conn.close()

    def get_by_username(self, username: str) -> dict[str, Any] | None:
        self.ensure_schema_and_seed()
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, password_salt, password_hash, display_name, role FROM account_user WHERE username=%s",
                    (username,),
                )
                row = cur.fetchone()
                if not row:
                    return None
                cols = [d[0] for d in cur.description]
                return dict(zip(cols, row))
        finally:
            conn.close()

    def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        self.ensure_schema_and_seed()
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, display_name, role FROM account_user WHERE user_id=%s",
                    (user_id,),
                )
                row = cur.fetchone()
                if not row:
                    return None
                cols = [d[0] for d in cur.description]
                return dict(zip(cols, row))
        finally:
            conn.close()

    def create(self, username: str, password: str, display_name: str, role: str) -> int:
        self.ensure_schema_and_seed()
        salt, digest = _hash_password(password)
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO account_user (username, password_salt, password_hash, display_name, role)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (username, salt, digest, display_name, role),
                )
                uid = int(cur.lastrowid)
            conn.commit()
            return uid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, user_id: int, display_name: str, role: str, password: str | None) -> bool:
        self.ensure_schema_and_seed()
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                if password:
                    salt, digest = _hash_password(password)
                    cur.execute(
                        "UPDATE account_user SET display_name=%s, role=%s, password_salt=%s, password_hash=%s WHERE user_id=%s",
                        (display_name, role, salt, digest, user_id),
                    )
                else:
                    cur.execute(
                        "UPDATE account_user SET display_name=%s, role=%s WHERE user_id=%s",
                        (display_name, role, user_id),
                    )
                ok = cur.rowcount > 0
            conn.commit()
            return ok
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, user_id: int) -> bool:
        self.ensure_schema_and_seed()
        conn = self._conn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM account_user WHERE user_id=%s", (user_id,))
                ok = cur.rowcount > 0
            conn.commit()
            return ok
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
