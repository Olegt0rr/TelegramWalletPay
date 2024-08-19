import json
from datetime import datetime
from uuid import uuid4

import pytest
from telegram_wallet_pay.tools import compute_signature

from tests.samples import WEBHOOK_MESSAGES


@pytest.fixture
def token() -> str:
    """Prepare token."""
    return str(uuid4())


@pytest.fixture
def path() -> str:
    """Prepare path."""
    return "/wallet"


@pytest.fixture
def body() -> str:
    """Prepare body."""
    return json.dumps(WEBHOOK_MESSAGES)


@pytest.fixture
def timestamp() -> str:
    """Prepare timestamp."""
    return str(datetime.now().timestamp())


@pytest.fixture
def signature(timestamp: str, body: str, token: str, path: str) -> str:
    """Prepare signature."""
    return compute_signature(
        store_api_key=token,
        http_method="POST",
        uri_path=path,
        timestamp=timestamp,
        body=body,
    )
