from __future__ import annotations

from typing import Any, Dict


def unwrap_data(payload: Any) -> Any:
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def as_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    raise TypeError("Expected dictionary response from API")
