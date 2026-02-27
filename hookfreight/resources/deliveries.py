from __future__ import annotations

from typing import Optional

from ..http import HttpClient
from ..pagination import MAX_LIMIT, clamp_pagination
from ..types import DeliveryListResponse, ListDeliveriesParams, PaginationParams, QueueStats
from ._common import as_dict, unwrap_data


class Deliveries:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, params: Optional[ListDeliveriesParams] = None) -> DeliveryListResponse:
        payload = self._http.get(
            "/deliveries",
            clamp_pagination(params, MAX_LIMIT["deliveries"]),
        )
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def list_by_event(
        self,
        event_id: str,
        params: Optional[PaginationParams] = None,
    ) -> DeliveryListResponse:
        payload = self._http.get(
            f"/events/{event_id}/deliveries",
            clamp_pagination(params, MAX_LIMIT["deliveries"]),
        )
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def retry(self, delivery_id: str) -> None:
        self._http.post(f"/deliveries/{delivery_id}/retry")

    def queue_stats(self) -> QueueStats:
        payload = self._http.get("/deliveries/queue/stats")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    # Backward-compatible aliases for mixed style call sites.
    def listByEvent(
        self,
        event_id: str,
        params: Optional[PaginationParams] = None,
    ) -> DeliveryListResponse:
        return self.list_by_event(event_id, params)

    def queueStats(self) -> QueueStats:
        return self.queue_stats()
