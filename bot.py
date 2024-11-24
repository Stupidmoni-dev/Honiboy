import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from telegram import Bot

# Replace these with your details
SOLANA_WALLET_ADDRESS = "C6KrAzXnYvBSpuDG9L2NpXe1vsFKk9kn3cLxFEB97Wjy"
TELEGRAM_BOT_TOKEN = "6673989012:AAE3kQp9nA82ZlG26e_RnnLOmWi0U2QaNnk"
TELEGRAM_CHAT_ID = "6216175814"

async def notify_via_telegram(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def monitor_wallet():
    client = AsyncClient("https://api.mainnet-beta.solana.com")
    previous_signature = None

    while True:
        try:
            # Fetch recent transactions for the wallet
            response = await client.get_signatures_for_address(SOLANA_WALLET_ADDRESS, limit=1)
            latest_transaction = response["result"][0] if response["result"] else None

            if latest_transaction:
                signature = latest_transaction["signature"]
                if signature != previous_signature:
                    previous_signature = signature
                    
                    # Get details of the transaction
                    tx_details = await client.get_confirmed_transaction(signature)
                    await notify_via_telegram(f"New transaction detected:\n{tx_details}")

            await asyncio.sleep(10)  # Check every 10 seconds
        except Exception as e:
            await notify_via_telegram(f"Error: {e}")
            await asyncio.sleep(30)  # Retry after 30 seconds if an error occurs

if __name__ == "__main__":
    asyncio.run(monitor_wallet())
