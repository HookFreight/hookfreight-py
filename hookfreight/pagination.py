from __future__ import annotations

from typing import Dict, Optional

from .types import PaginationParams

MAX_LIMIT = {
    "apps": 1000,
    "endpoints": 1000,
    "events": 50,
    "deliveries": 1000,
}


def clamp_pagination(
    params: Optional[PaginationParams],
    max_limit: int,
) -> Optional[Dict[str, object]]:
    if params is None:
        return None

    clamped: Dict[str, object] = dict(params)

    if "limit" in clamped and clamped["limit"] is not None:
        clamped["limit"] = max(1, min(max_limit, int(clamped["limit"])))

    if "offset" in clamped and clamped["offset"] is not None:
        clamped["offset"] = max(0, int(clamped["offset"]))

    return clamped
