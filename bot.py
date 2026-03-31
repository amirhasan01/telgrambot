import sys
sys.stdout.reconfigure(encoding='utf-8')

from telethon import TelegramClient
import requests
import asyncio

api_id = 36979235
api_hash = "6c17dfff0011cfe631a6f029f5fae3e6"

TOKEN = "1934568871:UAzs_KGSXXi8sZ-e8OdNVBLhko2cc0apn4E"

client = TelegramClient("session", api_id, api_hash)

last_update_id = None
DELETE_DELAY = 5  # seconds


async def send_message(chat_id, message):
    """Send a message to Bale bot."""
    url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=data).json()
    return response


async def delete_messages(chat_id, message_ids):
    """Delete a list of messages from Bale chat."""
    url = f"https://tapi.bale.ai/bot{TOKEN}/deleteMessage"
    for msg_id in message_ids:
        requests.post(url, json={"chat_id": chat_id, "message_id": msg_id})


async def get_last_10_messages(channel):
    """Fetch the last 10 posts from a Telegram channel and combine them."""
    try:
        messages = await client.get_messages(channel, limit=10)
        combined_text = ""
        for i, msg in enumerate(reversed(messages), start=1):
            text = msg.text if msg.text else "Media post (no text)"
            combined_text += f"{i}) {text}\n\n-----------------\n\n"
        return combined_text
    except Exception as e:
        return f"Error reading channel:\n{e}"


async def check_bale_messages():
    """Check for new commands from Bale and respond."""
    global last_update_id

    url = f"https://tapi.bale.ai/bot{TOKEN}/getUpdates"
    params = {}
    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(url, params=params).json()
    if response["ok"]:
        for update in response["result"]:
            last_update_id = update["update_id"]

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "").strip()

                if text:  # text is the channel name
                    # fetch messages from that Telegram channel
                    combined_posts = await get_last_10_messages(text)

                    # send combined message
                    sent_response = await send_message(chat_id, combined_posts)

                    # collect all message IDs in the chat (both user & bot)
                    all_message_ids = []

                    # user's command message
                    all_message_ids.append(update["message"]["message_id"])

                    # bot's message
                    if sent_response["ok"]:
                        all_message_ids.append(sent_response["result"]["message_id"])

                    # wait DELETE_DELAY seconds, then delete all messages together
                    await asyncio.sleep(DELETE_DELAY)
                    await delete_messages(chat_id, all_message_ids)


async def main():
    while True:
        try:
            await check_bale_messages()
        except Exception as e:
            print("ERROR:", e)
        await asyncio.sleep(2)  # check every 2 seconds


with client:
    client.loop.run_until_complete(main())
