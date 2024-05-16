from secrets import compare_digest
from typing import Optional

from fastapi import Depends, HTTPException, Request

from .signature import compute_signature


def get_timestamp(request: Request) -> str:
    """Get timestamp from header."""
    try:
        timestamp = request.headers["WalletPay-Timestamp"]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Timestamp header is missing",
        ) from None

    if not timestamp:
        raise HTTPException(
            status_code=400,
            detail="Timestamp header is empty",
        )

    return timestamp


def get_signature(request: Request) -> str:
    """Get signature from header."""
    try:
        signature = request.headers["WalletPay-Signature"]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Signature header is missing",
        ) from None

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Signature header is empty",
        )

    return signature


async def get_raw_body(request: Request) -> bytes:
    """Get request body."""
    return await request.body()


class CheckSignature:
    """Compare passed signature with computed signature."""

    def __init__(
        self,
        store_api_key: str,
        custom_exception: Optional[HTTPException] = None,
    ) -> None:
        self.__store_api_key = store_api_key
        self._exception = custom_exception or HTTPException(
            status_code=400,
            detail="Signature is not valid",
        )

    def __call__(
        self,
        request: Request,
        timestamp: str = Depends(get_timestamp),
        signature: str = Depends(get_signature),
        raw_body: bytes = Depends(get_raw_body),
    ) -> None:
        """Compare signatures."""
        valid_signature = compute_signature(
            store_api_key=self.__store_api_key,
            http_method=request.method,
            uri_path=request.url.path,
            timestamp=timestamp,
            body=raw_body,
        )

        if not compare_digest(signature, valid_signature):
            raise self._exception
