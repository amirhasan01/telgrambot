import sys
sys.stdout.reconfigure(encoding='utf-8')

from telethon import TelegramClient

api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

client = TelegramClient("session", api_id, api_hash)

async def main():
    messages = await client.get_messages("chekhabarre", limit=1)

    for msg in messages:
        print("Last message:")
        print(msg.text)

        # forward message to Saved Messages
        await client.forward_messages("me", msg)

with client:
    client.loop.run_until_complete(main())
