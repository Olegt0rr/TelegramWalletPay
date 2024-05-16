# Telegram Wallet Pay

Python async client for [Telegram Wallet Pay API](https://pay.wallet.tg) made of `aiohttp` and `pydantic`

**Also contains:**
 - `pydantic` models for every schema, even for incoming webhooks
 - signature validation tool, including ready-made `Depends` for `FastAPI`

[![Python](https://img.shields.io/pypi/pyversions/telegram-wallet-pay.svg)](https://pypi.org/project/telegram-wallet-pay/)
[![pypi](https://img.shields.io/pypi/v/telegram-wallet-pay?label=pypi%20package)](https://pypi.org/project/telegram-wallet-pay/)
[![Tests](https://github.com/Olegt0rr/TelegramWalletPay/actions/workflows/tests.yml/badge.svg)](https://github.com/Olegt0rr/TelegramWalletPay/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/codecov/c/github/Olegt0rr/TelegramWalletPay)](https://app.codecov.io/gh/Olegt0rr/TelegramWalletPay)

[![Code linter: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😎-FFDD67.svg)](https://gitmoji.dev)
---

## Get started

### Read Telegram Wallet Pay API docs

https://docs.wallet.tg/pay/#section/Get-started

### Install our library

```
pip install telegram-wallet-pay
```

### Create order

```python
import asyncio
import os
from uuid import uuid4

from telegram_wallet_pay import TelegramWalletPay

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Create order."""
    # create wallet client instance
    wallet = TelegramWalletPay(TOKEN)

    # create your first order
    response = await wallet.create_order(
        amount=40,
        currency_code="EUR",
        description="TestPayment",
        external_id=str(uuid4()),
        timeout_seconds=5 * 60,
        customer_telegram_user_id=66812456,
    )

    # let's print creation response
    print("Response:", response)
    print("Order:", response.data)

    # don't forget close API-client instance on your app shutdown
    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())

```


### Get order preview

```python
import asyncio
import os

from telegram_wallet_pay import TelegramWalletPay

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")


async def main() -> None:
    """Get order preview."""
    # create wallet client instance
    wallet = TelegramWalletPay(TOKEN)

    # get order preview
    response = await wallet.get_order_preview("<your-order-id>")

    # let's print received response
    print("Response:", response)
    print("Order Preview:", response.data)

    # don't forget close API-client instance on your app shutdown
    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())

```


## Other examples

* [Telegram bot example (aiogram)](./examples/02_telegram_bot.py)
* [Webhook handler example (FastAPI)](./examples/03_webhook_handler_fastapi.py)
* [Webhook handler example (aiohttp)](./examples/04_webhook_handler_aiohttp.py)

Also, feel free to open the
[folder with examples](https://github.com/Olegt0rr/TelegramWalletPay/tree/main/examples),
and if there is something missing there, describe your needs in [issue](https://github.com/Olegt0rr/TelegramWalletPay/issues/new/choose).
