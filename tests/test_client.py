import json
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

import pytest
from aresponses import ResponsesMockServer
from telegram_wallet_pay import TelegramWalletPay
from telegram_wallet_pay.errors import InvalidAPIKeyError
from telegram_wallet_pay.schemas import (
    CreateOrderResponse,
    GetOrderPreviewResponse,
    GetOrderReconciliationListResponse,
    MoneyAmount,
    OrderAmount,
    OrderAmountResponse,
    OrderPreview,
    OrderReconciliationItem,
    OrderReconciliationList,
)

ORDER_PREVIEW = OrderPreview(
    id="",
    status="ACTIVE",
    number="",
    amount=MoneyAmount(currency_code="EUR", amount="42.0"),
    created_datetime=datetime.now(),
    expiration_datetime=datetime.now(),
    pay_link="",
    direct_pay_link="",
)

CREATE_ORDER_RESPONSE = CreateOrderResponse(
    status="SUCCESS",
    message="",
    data=ORDER_PREVIEW,
)

GET_ORDER_PREVIEW_RESPONSE = GetOrderPreviewResponse(
    status="SUCCESS",
    message="",
    data=ORDER_PREVIEW,
)

ORDER_RECONCILIATION_ITEM = OrderReconciliationItem(
    id=42,
    status="EXPIRED",
    amount=MoneyAmount(currency_code="EUR", amount="42.0"),
    external_id="",
    created_datetime=datetime.now(),
    expiration_datetime=datetime.now(),
)

GET_ORDERS_LIST_RESPONSE = GetOrderReconciliationListResponse(
    status="SUCCESS",
    message=None,
    data=OrderReconciliationList(items=[]),
)

ORDER_AMOUNT_RESPONSE = OrderAmountResponse(
    status="SUCCESS",
    message="",
    data=OrderAmount(total_amount=42),
)


@pytest.fixture
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
                text=CREATE_ORDER_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        response = await wallet.create_order(
            amount=ORDER_PREVIEW.amount.amount,
            currency_code=ORDER_PREVIEW.amount.currency_code,
            description="description",
            external_id="",
            timeout_seconds=30,
            customer_telegram_user_id=42,
        )
        assert response == CREATE_ORDER_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestGetOrderPreview:
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
                text=GET_ORDER_PREVIEW_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        response = await wallet.get_order_preview(ORDER_PREVIEW.id)
        assert response == GET_ORDER_PREVIEW_RESPONSE
        aresponses.assert_plan_strictly_followed()

    async def test_invalid_token(
        self,
        wallet: TelegramWalletPay,
        aresponses: ResponsesMockServer,
    ) -> None:
        """Test successful getting Order preview."""
        aresponses.add(
            path_pattern=self.URI,
            method_pattern=self.METHOD,
            response=aresponses.Response(
                text=json.dumps({"success": False, "error": "Invalid token"}),
                content_type="application/json",
                status=401,
            ),
        )
        with pytest.raises(InvalidAPIKeyError):
            await wallet.get_order_preview(ORDER_PREVIEW.id)

        aresponses.assert_plan_strictly_followed()

    async def test_deprecated(
        self,
        wallet: TelegramWalletPay,
        aresponses: ResponsesMockServer,
    ) -> None:
        """Test getting Order preview with deprecated method."""
        aresponses.add(
            path_pattern=self.URI,
            method_pattern=self.METHOD,
            response=aresponses.Response(
                text=GET_ORDER_PREVIEW_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        with pytest.warns(
            DeprecationWarning,
            match="Method .* is deprecated",
        ):
            response = await wallet.get_preview(ORDER_PREVIEW.id)

        assert response == GET_ORDER_PREVIEW_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestGetOrderList:
    METHOD = "GET"
    URI = "/wpay/store-api/v1/reconciliation/order-list"

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
                text=GET_ORDERS_LIST_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        response = await wallet.get_order_list(offset=0, count=10)
        assert response == GET_ORDERS_LIST_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestGetOrderAmount:
    METHOD = "GET"
    URI = "/wpay/store-api/v1/reconciliation/order-amount"

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
                text=ORDER_AMOUNT_RESPONSE.model_dump_json(by_alias=True),
                content_type="application/json",
                status=200,
            ),
        )
        response = await wallet.get_order_amount()
        assert response == ORDER_AMOUNT_RESPONSE
        aresponses.assert_plan_strictly_followed()


class TestSession:
    async def test_close_without_session(self, wallet: TelegramWalletPay) -> None:
        """Test session close without any request."""


@pytest.mark.parametrize("token", [None, bool, 42])
def test_client_init_without_token(token: Any) -> None:
    """Check passed token is string and not empty."""
    msg = f"String token should be provided. You passed: {token!r}"
    with pytest.raises(RuntimeError, match=msg):
        # noinspection PyTypeChecker
        TelegramWalletPay(token)
