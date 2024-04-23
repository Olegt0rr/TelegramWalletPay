import hashlib
import hmac
from base64 import b64encode
from typing import Union

ENCODING = "utf-8"


def compute_signature(
    store_api_key: str,
    http_method: str,
    uri_path: str,
    timestamp: str,
    body: Union[str, bytes],
) -> str:
    """Compute signature."""
    if not store_api_key:
        msg = f"Argument 'store_api_key' should not be empty. Passed {store_api_key=}"
        raise ValueError(msg)

    if isinstance(body, str):
        body = bytes(body, ENCODING)

    body_base64 = b64encode(body).decode(ENCODING)
    payload = f"{http_method}.{uri_path}.{timestamp}.{body_base64}"

    signature_bytes = hmac.new(
        key=bytes(store_api_key, ENCODING),
        msg=bytes(payload, ENCODING),
        digestmod=hashlib.sha256,
    ).digest()

    return b64encode(signature_bytes).decode(ENCODING)
