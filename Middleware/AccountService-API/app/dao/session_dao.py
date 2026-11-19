"""In-memory session tokens for local AccountService auth."""

from __future__ import annotations

import secrets
from typing import Protocol


class SessionDao(Protocol):
    def create(self, username: str, role: str) -> str: ...
    def get(self, token: str) -> dict | None: ...
    def revoke(self, token: str) -> bool: ...


class MemorySessionDao:
    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def create(self, username: str, role: str) -> str:
        token = secrets.token_urlsafe(32)
        self._sessions[token] = {"username": username, "role": role}
        return token

    def get(self, token: str) -> dict | None:
        return self._sessions.get(token)

    def revoke(self, token: str) -> bool:
        return self._sessions.pop(token, None) is not None
