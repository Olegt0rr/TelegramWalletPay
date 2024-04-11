from telegram_wallet_pay.tools import compute_signature


def test_signature() -> None:
    """Test signature provided by docs."""
    body = (
        '[{"eventDateTime":"2023-07-28T10:20:17.681338Z",'
        '"eventId":10030477545046017,"type":"ORDER_PAID","payload":{'
        '"id":10030467668508673,"number":"XYTNJP2O","customData":"in exercitation '
        'culpa","externalId":"JDF23NN","orderAmount":{"amount":"0.100000340",'
        '"currencyCode":"TON"},"selectedPaymentOption":{"amount":{'
        '"amount":"0.132653","currencyCode":"USDT"},"amountFee":{'
        '"amount":"0.001327","currencyCode":"USDT"},"amountNet":{'
        '"amount":"0.131326","currencyCode":"USDT"},'
        '"exchangeRate":"1.3265247467314987"},'
        '"orderCompletedDateTime":"2023-07-28T10:20:17.628946Z"}}]'
    )

    signature = compute_signature(
        store_api_key="your_secret_api_key_sYIpNypce5sls6Ik",
        http_method="POST",
        uri_path="/webhook/",
        timestamp="168824905680291",
        body=body,
    )

    assert signature == "MGfJzeEprADZbihhRcGcCY5pYTI/IEJ91ejyA+XOWAs="
