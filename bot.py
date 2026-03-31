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


async def get_last_10_messages(channel):
    try:
        messages = await client.get_messages(channel, limit=50)
        combined_text = ""
        for i, msg in enumerate(reversed(messages), start=1):
            text = msg.text if msg.text else "Media post (no text)"
            combined_text += f"{i}) {text}\n\n-----------------\n\n"
        return combined_text
    except:
        return None  # do nothing if channel not valid


async def send_combined_and_delete(chat_id, combined_text, command_message_id):
    if not combined_text:
        return

    # Send combined message
    send_url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": combined_text}
    response = requests.post(send_url, json=data).json()

    if response["ok"]:
        message_id = response["result"]["message_id"]

        await asyncio.sleep(10)

        # Delete both user command and bot message
        delete_url = f"https://tapi.bale.ai/bot{TOKEN}/deleteMessage"
        for msg_id in [message_id, command_message_id]:
            requests.post(delete_url, json={"chat_id": chat_id, "message_id": msg_id})


async def check_bale_messages():
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
                command_message_id = update["message"]["message_id"]

                if text:
                    # text is considered the channel name
                    combined_posts = await get_last_10_messages(text)
                    if combined_posts:
                        await send_combined_and_delete(chat_id, combined_posts, command_message_id)
                    # do nothing if channel is invalid


async def main():
    while True:
        try:
            await check_bale_messages()
        except:
            pass  # ignore all errors silently
        await asyncio.sleep(3)


with client:
    client.loop.run_until_complete(main())
