import asyncio
import ssl
import warnings
from contextlib import asynccontextmanager
from decimal import Decimal
from http import HTTPStatus
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Literal,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

import certifi
from aiohttp import ClientResponse, ClientSession, TCPConnector
from pydantic import BaseModel

from telegram_wallet_pay.enums import Currency
from telegram_wallet_pay.errors import (
    InvalidAPIKeyError,
    InvalidRequestError,
    NotFountError,
    RequestLimitReachedError,
    TelegramWalletPayError,
    UnexpectedError,
)
from telegram_wallet_pay.schemas import (
    CreateOrderRequest,
    CreateOrderResponse,
    GetOrderPreviewResponse,
    GetOrderReconciliationListResponse,
    MoneyAmount,
    OrderAmountResponse,
)

T = TypeVar("T", bound=BaseModel)

AUTH_HEADER = "Wpay-Store-Api-Key"
DEFAULT_API_HOST = "https://pay.wallet.tg"

EXCEPTIONS_MAPPING: Dict[Union[HTTPStatus, int], Type[TelegramWalletPayError]] = {
    HTTPStatus.BAD_REQUEST: InvalidRequestError,
    HTTPStatus.UNAUTHORIZED: InvalidAPIKeyError,
    HTTPStatus.NOT_FOUND: NotFountError,
    HTTPStatus.TOO_MANY_REQUESTS: RequestLimitReachedError,
    HTTPStatus.INTERNAL_SERVER_ERROR: UnexpectedError,
}


class TelegramWalletPay:
    """Telegram Wallet API client."""

    def __init__(self, token: str, api_host: str = DEFAULT_API_HOST) -> None:
        if not token or not isinstance(token, str):
            msg = f"String token should be provided. You passed: {token}"
            raise RuntimeError(msg)

        self._base_url = api_host
        self._session: Optional[ClientSession] = None
        self._headers = {AUTH_HEADER: token}

    async def create_order(  # noqa: PLR0913
        self,
        *,
        amount: Union[str, Decimal, float],
        currency_code: Literal[
            Currency.TON,
            Currency.NOT,
            Currency.BTC,
            Currency.USDT,
            Currency.EUR,
            Currency.USD,
            Currency.RUB,
        ],
        description: str,
        external_id: str,
        timeout_seconds: int,
        customer_telegram_user_id: int,
        auto_conversion_currency: Optional[
            Literal[
                Currency.TON,
                Currency.NOT,
                Currency.BTC,
                Currency.USDT,
            ]
        ] = None,
        return_url: Optional[str] = None,
        fail_return_url: Optional[str] = None,
        custom_data: Optional[str] = None,
    ) -> CreateOrderResponse:
        """Create an order.

        Docs:
        https://docs.wallet.tg/pay/#tag/Order/operation/create
        """
        create_order_request = CreateOrderRequest(
            amount=MoneyAmount(
                amount=str(amount),
                currency_code=currency_code,
            ),
            auto_conversion_currency=auto_conversion_currency,
            description=description,
            return_url=return_url,
            fail_return_url=fail_return_url,
            custom_data=custom_data,
            external_id=external_id,
            timeout_seconds=timeout_seconds,
            customer_telegram_user_id=customer_telegram_user_id,
        )

        async with self._make_request(
            method="POST",
            url="/wpay/store-api/v1/order",
            json=create_order_request.model_dump(by_alias=True),
        ) as response:
            return await self._prepare_result(response, CreateOrderResponse)

    async def get_preview(self, order_id: str) -> GetOrderPreviewResponse:
        """Retrieve the order information.

        Deprecated! Use method `.get_order_preview()` instead.
        """
        warnings.warn(
            "Method `.get_preview()` is deprecated and will be removed in v1.0.0\n"
            "Use method `.get_order_preview()` instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return await self.get_order_preview(order_id)

    async def get_order_preview(self, order_id: str) -> GetOrderPreviewResponse:
        """Retrieve the order information.

        Docs:
        https://docs.wallet.tg/pay/#tag/Order/operation/getPreview
        """
        async with self._make_request(
            method="GET",
            url="/wpay/store-api/v1/order/preview",
            params={"id": order_id},
        ) as response:
            return await self._prepare_result(response, GetOrderPreviewResponse)

    async def get_order_list(
        self,
        *,
        offset: int,
        count: int,
    ) -> GetOrderReconciliationListResponse:
        """Get list of store orders.

        Items sorted by creation time in ascending order.

        Docs:
        https://docs.wallet.tg/pay/#tag/Order-Reconciliation/operation/getOrderList
        """
        query_params: Dict[str, Any] = {
            "offset": offset,
            "count": count,
        }

        async with self._make_request(
            method="GET",
            url="/wpay/store-api/v1/reconciliation/order-list",
            params=query_params,
        ) as response:
            return await self._prepare_result(
                response,
                GetOrderReconciliationListResponse,
            )

    async def get_order_amount(self) -> OrderAmountResponse:
        """Get total count of all created orders in the Store.

        Including all - paid and unpaid.

        Docs:
        https://docs.wallet.tg/pay/#tag/Order-Reconciliation/operation/getOrderAmount
        """
        async with self._make_request(
            method="GET",
            url="/wpay/store-api/v1/reconciliation/order-amount",
        ) as response:
            return await self._prepare_result(response, OrderAmountResponse)

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            return

        await self._session.close()

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None or self._session.closed:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = TCPConnector(ssl=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                headers=self._headers,
            )

        return self._session

    @asynccontextmanager
    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, str]] = None,
        json: Optional[Mapping[str, str]] = None,
    ) -> AsyncIterator[ClientResponse]:
        """Make request with cached session."""
        session = await self._get_session()
        async with session.request(
            method=method,
            url=url,
            params=params,
            json=json,
        ) as response:
            yield response

    @staticmethod
    async def _prepare_result(response: ClientResponse, schema: Type[T]) -> T:
        """Prepare response result or raise an exception."""
        status = response.status
        body = await response.text()

        if status == HTTPStatus.OK:
            return schema.model_validate_json(body)

        exc_type = EXCEPTIONS_MAPPING.get(status, TelegramWalletPayError)
        raise exc_type(body)
