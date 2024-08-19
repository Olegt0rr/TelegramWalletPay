import logging
from typing import Dict

import pytest
from fastapi import Depends, FastAPI, status
from fastapi.testclient import TestClient
from telegram_wallet_pay.schemas import WebhookMessages
from telegram_wallet_pay.tools.fastapi import CheckSignature

logger = logging.getLogger(__name__)


@pytest.fixture
def app(token: str, path: str) -> FastAPI:
    """Prepare FastAPI application."""
    application = FastAPI()
    check_signature = CheckSignature(token)

    @application.post(path, dependencies=[Depends(check_signature)])
    async def webhook_handler(webhook_messages: WebhookMessages) -> Dict[str, bool]:
        logger.info("Get webhook_messages: %s", webhook_messages)
        return {"success": True}

    return application


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Prepare test client."""
    return TestClient(app)


def test_success(
    client: TestClient,
    signature: str,
    body: str,
    timestamp: str,
    path: str,
) -> None:
    """Test success case."""
    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": signature,
    }
    response = client.post(path, headers=headers, content=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"success": True}


def test_timestamp_missing(
    client: TestClient,
    signature: str,
    path: str,
) -> None:
    headers = {
        "WalletPay-Signature": signature,
    }
    response = client.post(path, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Timestamp header is missing"}


def test_timestamp_empty(
    client: TestClient,
    signature: str,
    path: str,
) -> None:
    headers = {
        "WalletPay-Timestamp": "",
        "WalletPay-Signature": signature,
    }
    response = client.post(path, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Timestamp header is empty"}


def test_signature_missing(
    client: TestClient,
    path: str,
    timestamp: str,
) -> None:
    headers = {
        "WalletPay-Timestamp": timestamp,
    }
    response = client.post(path, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Signature header is missing"}


def test_signature_empty(
    client: TestClient,
    path: str,
    timestamp: str,
) -> None:
    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": "",
    }
    response = client.post(path, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Signature header is empty"}


def test_signature_invalid(
    client: TestClient,
    path: str,
    timestamp: str,
) -> None:
    headers = {
        "WalletPay-Timestamp": timestamp,
        "WalletPay-Signature": "invalid-signature",
    }
    response = client.post(path, headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Signature is not valid"}
