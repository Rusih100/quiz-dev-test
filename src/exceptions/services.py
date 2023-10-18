from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException


class BaseError(HTTPException):
    detail = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: Optional[dict[str, str]] = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class ServiceError(BaseError):
    detail = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers: Optional[dict[str, str]] = None
