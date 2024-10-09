import json
from collections.abc import Awaitable
from functools import wraps
from secrets import compare_digest
from typing import Callable, Optional, TypeVar

from aiohttp import web

from .signature import compute_signature

Request = TypeVar("Request", bound=web.Request)
Response = TypeVar("Response", bound=web.StreamResponse)
Handler = Callable[..., Awaitable[Response]]


def get_signature(request: web.Request) -> str:
    """Get signature from header."""
    try:
        signature = request.headers["WalletPay-Signature"]
    except KeyError:
        raise web.HTTPBadRequest(
            text=json.dumps({"detail": "Signature header is missing"}),
            content_type="application/json",
        ) from None

    if not signature:
        raise web.HTTPBadRequest(
            text=json.dumps({"detail": "Signature header is empty"}),
            content_type="application/json",
        )

    return signature


def get_timestamp(request: web.Request) -> str:
    """Get timestamp from header."""
    try:
        timestamp = request.headers["WalletPay-Timestamp"]
    except KeyError:
        raise web.HTTPBadRequest(
            text=json.dumps({"detail": "Timestamp header is missing"}),
            content_type="application/json",
        ) from None

    if not timestamp:
        raise web.HTTPBadRequest(
            text=json.dumps({"detail": "Timestamp header is empty"}),
            content_type="application/json",
        )

    return timestamp


def check_signature(
    store_api_key: str,
    custom_exception: Optional[web.HTTPClientError] = None,
) -> Callable:
    """Decorate aiohttp handler to check signature first."""
    exception = custom_exception or web.HTTPBadRequest(
        text=json.dumps({"detail": "Signature is not valid"}),
        content_type="application/json",
    )

    def decorator(handler: Handler) -> Handler:
        @wraps(handler)
        async def wrapper(
            request: web.Request,
            *args,
            **kwargs,
        ) -> Response:
            """Check signature."""
            signature = get_signature(request)
            timestamp = get_timestamp(request)
            raw_body = await request.text()

            valid_signature = compute_signature(
                store_api_key=store_api_key,
                http_method=request.method,
                uri_path=request.url.path,
                timestamp=timestamp,
                body=raw_body,
            )

            if not compare_digest(signature, valid_signature):
                raise exception

            return await handler(request, *args, **kwargs)

        return wrapper

    return decorator
