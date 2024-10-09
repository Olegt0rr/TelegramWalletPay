import os

import uvicorn
from fastapi import Depends, FastAPI
from telegram_wallet_pay.schemas import WebhookMessages
from telegram_wallet_pay.tools.fastapi import CheckSignature

# store TELEGRAM_WALLET_PAY_TOKEN to your .env
# wallet token can be issued via https://pay.wallet.tg/
TELEGRAM_WALLET_PAY_TOKEN = os.getenv("TELEGRAM_WALLET_PAY_TOKEN")

app = FastAPI()
check_signature = CheckSignature(TELEGRAM_WALLET_PAY_TOKEN)


@app.post("/wallet", dependencies=[Depends(check_signature)])
async def webhook_handler(webhook_messages: WebhookMessages) -> dict[str, bool]:
    """Handle webhook from Telegram Wallet API."""
    for webhook_message in webhook_messages:
        # process every webhook message as you wish
        # e.g. store them to your database. We just print it here
        print(f"Received webhook message: {webhook_message}")

    return {"success": True}


if __name__ == "__main__":
    uvicorn.run(app)
