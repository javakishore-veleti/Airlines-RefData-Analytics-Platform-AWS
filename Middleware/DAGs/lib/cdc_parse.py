"""Parse Debezium MySQL CDC envelopes into lake row operations (story #27)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class LakeOp:
    op: str  # insert | update | delete
    rule_id: int
    row: dict[str, Any] | None


def map_debezium_op(payload: Mapping[str, Any]) -> LakeOp | None:
    """Map Debezium envelope `op` field to lake semantics.

    c → insert, u → update, d → delete, r → insert (snapshot read).
    """
    if not payload:
        return None
    # Flatten if envelope has "payload" wrapper
    body = payload.get("payload", payload)
    op_code = body.get("op")
    if op_code is None:
        return None
    before = body.get("before")
    after = body.get("after")
    if op_code in ("c", "r"):
        if not after or "rule_id" not in after:
            return None
        return LakeOp(op="insert", rule_id=int(after["rule_id"]), row=dict(after))
    if op_code == "u":
        if not after or "rule_id" not in after:
            return None
        return LakeOp(op="update", rule_id=int(after["rule_id"]), row=dict(after))
    if op_code == "d":
        src = before or {}
        if "rule_id" not in src:
            return None
        return LakeOp(op="delete", rule_id=int(src["rule_id"]), row=None)
    return None
