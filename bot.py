from telethon import TelegramClient, events

api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

client = TelegramClient("session_name", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.raw_text == "hi":
        await event.reply("Hello!")

client.start()
client.run_until_disconnected()
