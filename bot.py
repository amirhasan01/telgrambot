from telethon import TelegramClient

# Use your existing API ID and API HASH
api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

# Connect using your session file
client = TelegramClient("session", api_id, api_hash)

async def main():
    # Send a message to yourself
    me = await client.get_me()
    await client.send_message(me.id, "Hello! This is a test message from my bot.")

with client:
    client.loop.run_until_complete(main())
