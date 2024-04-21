import hashlib
import hmac
from base64 import b64encode
from typing import Union

ENCODING = "utf-8"


def from_snake_to_pascal(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def from_snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    if "_" not in snake_str:
        return snake_str
    camel_string = from_snake_to_pascal(snake_str)
    return snake_str[0].lower() + camel_string[1:]


def compute_signature(
    store_api_key: str,
    http_method: str,
    uri_path: str,
    timestamp: str,
    body: Union[str, bytes],
) -> str:
    """Compute signature."""
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
