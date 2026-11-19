from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class HealthReq:
    pass

@dataclass
class HealthResp:
    status: str = "unknown"
    mysql: bool = False
    detail: Optional[str] = None

@dataclass
class HealthCtx:
    req: HealthReq = field(default_factory=HealthReq)
    resp: HealthResp = field(default_factory=HealthResp)


@dataclass
class UserReq:
    user_id: int | None = None
    username: str = ""
    password: str = ""
    display_name: str = ""
    role: str = "operator"


@dataclass
class UserResp:
    ok: bool = False
    user_id: int | None = None
    username: str = ""
    display_name: str = ""
    role: str = ""
    users: list = field(default_factory=list)
    message: str = ""


@dataclass
class UserCtx:
    req: UserReq = field(default_factory=UserReq)
    resp: UserResp = field(default_factory=UserResp)


@dataclass
class AuthReq:
    username: str = ""
    password: str = ""
    token: str = ""
    display_name: str = ""


@dataclass
class AuthResp:
    ok: bool = False
    token: str = ""
    username: str = ""
    role: str = ""
    message: str = ""


@dataclass
class AuthCtx:
    req: AuthReq = field(default_factory=AuthReq)
    resp: AuthResp = field(default_factory=AuthResp)
