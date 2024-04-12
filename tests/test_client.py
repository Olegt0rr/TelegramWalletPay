from datetime import datetime
from typing import AsyncIterator

import pytest
from aresponses import ResponsesMockServer
from telegram_wallet_pay import TelegramWalletPay
from telegram_wallet_pay.schemas import MoneyAmount, OrderPreview, OrderResult

SUCCESS_ORDER_PREVIEW = OrderPreview(
    id="",
    status="ACTIVE",
    number="",
    amount=MoneyAmount(currency_code="RUB", amount="42.0"),
    created_datetime=datetime.now(),
    expiration_datetime=datetime.now(),
    pay_link="",
    direct_pay_link="",
)

SUCCESS_RESPONSE = OrderResult(
    status="SUCCESS",
    message="",
    data=SUCCESS_ORDER_PREVIEW,
)


@pytest.fixture()
async def wallet() -> AsyncIterator[TelegramWalletPay]:
    """Prepare TelegramWalletPay fixture."""
    wallet = TelegramWalletPay("TOKEN")
    yield wallet
    await wallet.close()


class TestCreateOrder:
    METHOD = "POST"
    URI = "/wpay/store-api/v1/order"

    async def test_success(
        self,
        wallet: TelegramWalletPay,
        aresponses: ResponsesMockServer,
    ) -> None:
        """Test successful Order creation."""
        aresponses.add(
            path_pattern=self.URI,
            method_pattern=self.METHOD,
            response=aresponses.Response(
                text=SUCCESS_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        result = await wallet.create_order(
            amount=SUCCESS_ORDER_PREVIEW.amount.amount,
            currency_code=SUCCESS_ORDER_PREVIEW.amount.currency_code,
            description="description",
            external_id="",
            timeout_seconds=30,
            customer_telegram_user_id=42,
        )
        assert result == SUCCESS_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestGetPreview:
    METHOD = "GET"
    URI = "/wpay/store-api/v1/order/preview"

    async def test_success(
        self,
        wallet: TelegramWalletPay,
        aresponses: ResponsesMockServer,
    ) -> None:
        """Test successful getting Order preview."""
        aresponses.add(
            path_pattern=self.URI,
            method_pattern=self.METHOD,
            response=aresponses.Response(
                text=SUCCESS_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        result = await wallet.get_preview(SUCCESS_ORDER_PREVIEW.id)
        assert result == SUCCESS_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestSession:
    async def test_close_without_session(self, wallet: TelegramWalletPay) -> None:
        """Test session close without any request."""
