import logging
from typing import Awaitable, Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from telegram_wallet_pay.schemas import WebhookMessages
from telegram_wallet_pay.tools.aiohttp import check_signature

ClientFixture = Callable[[web.Application], Awaitable[TestClient]]
OK = 200
BAD_REQUEST = 400

logger = logging.getLogger(__name__)


@pytest.fixture
async def app(path: str, handler: Callable) -> web.Application:
    app = web.Application()
    app.router.add_route("POST", path, handler)
    yield app
    await app.cleanup()


@pytest.fixture
async def client(app: web.Application, aiohttp_client: ClientFixture) -> TestClient:
    client = await aiohttp_client(app)
    yield client
    await client.close()


@pytest.fixture
async def handler(token: str) -> Callable:
    @check_signature(token)
    async def handler(request: web.Request) -> web.StreamResponse:
        json_data = await request.text()
        webhook_messages = WebhookMessages.model_validate_json(json_data)
        logger.info("Got webhook messages: %s", webhook_messages)
        return web.json_response({"success": True})

    return handler


async def test_success(
    signature: str,
    body: str,
    timestamp: str,
    path: str,
    client: TestClient,
) -> None:
    """Test success case."""

    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": signature,
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == OK


async def test_timestamp_missing(
    signature: str,
    body: str,
    path: str,
    client: TestClient,
) -> None:
    """Test timestamp missing case."""
    headers = {
        "WalletPay-Signature": signature,
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == BAD_REQUEST
    assert await response.json() == {"detail": "Timestamp header is missing"}


async def test_timestamp_empty(
    signature: str,
    body: str,
    path: str,
    client: TestClient,
) -> None:
    """Test timestamp is empty case."""

    headers = {
        "WalletPay-Timestamp": "",
        "WalletPay-Signature": signature,
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == BAD_REQUEST
    assert await response.json() == {"detail": "Timestamp header is empty"}


async def test_signature_missing(
    body: str,
    timestamp: str,
    path: str,
    client: TestClient,
) -> None:
    """Test signature is missing case."""

    headers = {
        "WalletPay-Timestamp": timestamp,
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == BAD_REQUEST
    assert await response.json() == {"detail": "Signature header is missing"}


async def test_signature_empty(
    body: str,
    timestamp: str,
    path: str,
    client: TestClient,
) -> None:
    """Test signature is empty case."""

    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": "",
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == BAD_REQUEST
    assert await response.json() == {"detail": "Signature header is empty"}


async def test_signature_invalid(
    body: str,
    timestamp: str,
    path: str,
    client: TestClient,
) -> None:
    """Test signature is invalid case."""

    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": "invalid-signature",
    }
    response = await client.post(path=path, data=body, headers=headers)
    assert response.status == BAD_REQUEST
    assert await response.json() == {"detail": "Signature is not valid"}
