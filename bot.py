import sys
sys.stdout.reconfigure(encoding='utf-8')

from telethon import TelegramClient
import requests

# Telegram API info
api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

# Bale bot info
TOKEN = "1934568871:UAzs_KGSXXi8sZ-e8OdNVBLhko2cc0apn4E"
CHAT_ID = 650686292

client = TelegramClient("session", api_id, api_hash)


async def main():
    messages = await client.get_messages("chekhabarre", limit=1)

    for msg in messages:
        print("Last message:")
        print(msg.text)

        # Forward to Telegram Saved Messages
        await client.forward_messages("me", msg)

        # Send to Bale bot
        bale_url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": msg.text
        }

        response = requests.post(bale_url, json=data)
        print("Bale response:", response.text)


with client:
    client.loop.run_until_complete(main())
