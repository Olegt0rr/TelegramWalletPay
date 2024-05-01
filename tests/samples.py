ORDER_AMOUNT = {
    "currencyCode": "RUB",
    "amount": "40.00",
}

SELECTED_PAYMENT_OPTION = {
    "amount": {
        "currencyCode": "TON",
        "amount": "0.069848094",
    },
    "amountFee": {
        "currencyCode": "TON",
        "amount": "0.000698481",
    },
    "amountNet": {
        "currencyCode": "TON",
        "amount": "0.069149613",
    },
    "exchangeRate": "0.0017462023476135017",
}

WEBHOOK_PAYLOAD = {
    "id": 10829787081217,
    "number": "E953D09Q",
    "externalId": "0120bb34-5a74-4eb2-a3da-774b97cf3fbe",
    "orderAmount": ORDER_AMOUNT,
    "selectedPaymentOption": SELECTED_PAYMENT_OPTION,
    "orderCompletedDateTime": "2024-04-21T15:04:24.092Z",
}

WEBHOOK_MESSAGE_ORDER_PAID = {
    "eventDateTime": "2024-04-21T15:04:24.092Z",
    "eventId": 10829789207553,
    "type": "ORDER_PAID",
    "payload": WEBHOOK_PAYLOAD,
}

WEBHOOK_MESSAGE_ORDER_FAILED = {
    "eventId": 11044361216001,
    "eventDateTime": "2024-05-01T07:53:56.000991Z",
    "payload": {
        "id": 11000119772673,
        "number": "LVDPW6K8",
        "status": "EXPIRED",
        "customData": "some-custom-data",
        "externalId": "07d9539e-fd61-497e-a164-d2e354a55744",
        "orderAmount": {
            "amount": "0.44",
            "currencyCode": "USD",
        },
        "orderCompletedDateTime": "2024-05-01T07:53:56.000980Z",
    },
    "type": "ORDER_FAILED",
}

WEBHOOK_MESSAGES = [WEBHOOK_MESSAGE_ORDER_PAID, WEBHOOK_MESSAGE_ORDER_FAILED]
