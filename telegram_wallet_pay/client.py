import asyncio
import logging
import ssl
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import AsyncIterator, Literal, Mapping, Optional, Union

from aiohttp import ClientResponse, ClientSession, TCPConnector

from telegram_wallet_pay.schemas import MoneyAmount, OrderNew, OrderResult

AUTH_HEADER = "Wpay-Store-Api-Key"
DEFAULT_API_HOST = "https://pay.wallet.tg"


class TelegramWalletPay:
    """Telegram Wallet API client."""

    async def create_order(  # noqa: PLR0913
        self,
        amount: Union[str, Decimal, float],
        currency_code: Literal["TON", "BTC", "USDT", "EUR", "USD", "RUB"],
        description: str,
        external_id: str,
        timeout_seconds: int,
        customer_telegram_user_id: int,
        auto_conversion_currency: Optional[Literal["TON", "BTC", "USDT"]] = None,
        return_url: Optional[str] = None,
        fail_return_url: Optional[str] = None,
        custom_data: Optional[str] = None,
    ) -> OrderResult:
        """Create an order."""
        order_new = OrderNew(
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
            json=order_new.model_dump(by_alias=True),
        ) as response:  # type: ClientResponse
            json_data = await response.text()
            self.log.info("Received answer: %s", json_data)

        return OrderResult.model_validate_json(json_data)

    async def get_preview(self, order_id: str) -> OrderResult:
        """Retrieve the order information."""
        async with self._make_request(
            method="GET",
            url="/wpay/store-api/v1/order/preview",
            params={"id": order_id},
        ) as response:  # type: ClientResponse
            json_data = await response.text()

        return OrderResult.model_validate_json(json_data)

    def __init__(self, token: str, api_host: str = DEFAULT_API_HOST) -> None:
        self.log = logging.getLogger(self.__class__.__name__)

        self._base_url = api_host
        self._session: Optional[ClientSession] = None
        self._headers = {AUTH_HEADER: token}

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None or self._session.closed:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_default_certs()
            connector = TCPConnector(ssl_context=ssl_context)
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
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(method, url, params=params, json=json) as response:
            yield response

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
