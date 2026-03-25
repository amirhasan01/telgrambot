import sys
sys.stdout.reconfigure(encoding='utf-8')

from telethon import TelegramClient
import requests
import asyncio

api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

TOKEN = "1934568871:UAzs_KGSXXi8sZ-e8OdNVBLhko2cc0apn4E"
CHAT_ID = 123456789   # replace with your real Bale chat_id

client = TelegramClient("session", api_id, api_hash)


async def main():
    while True:
        try:
            messages = await client.get_messages("chekhabarre", limit=1)

            msg = messages[0]

            text = msg.text if msg.text else "Media post (no text)"

            print("Last message:")
            print(text)

            await client.forward_messages("me", msg)

            bale_url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": text
            }

            response = requests.post(bale_url, json=data, timeout=10)

            print("Bale response:", response.text)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(60)  # check every 60 seconds


with client:
    client.loop.run_until_complete(main())
