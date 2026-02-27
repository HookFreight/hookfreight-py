from __future__ import annotations

from typing import Any, Optional

from ..http import HttpClient
from ..pagination import MAX_LIMIT, clamp_pagination
from ..types import (
    App,
    AppDeleteResponse,
    AppListResponse,
    CreateAppParams,
    PaginationParams,
    UpdateAppParams,
)
from ._common import as_dict, unwrap_data


class Apps:
    def __init__(self, http: HttpClient):
        self._http = http

    def list(self, params: Optional[PaginationParams] = None) -> AppListResponse:
        payload = self._http.get("/apps", clamp_pagination(params, MAX_LIMIT["apps"]))
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def create(self, params: CreateAppParams) -> App:
        payload = self._http.post("/apps", params)
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def get(self, app_id: str) -> App:
        payload = self._http.get(f"/apps/{app_id}")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def update(self, app_id: str, params: UpdateAppParams) -> App:
        payload = self._http.put(f"/apps/{app_id}", params)
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]

    def delete(self, app_id: str) -> AppDeleteResponse:
        payload = self._http.delete(f"/apps/{app_id}")
        return as_dict(unwrap_data(payload))  # type: ignore[return-value]
