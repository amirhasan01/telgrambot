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

DELETE_DELAY = 5  # seconds before deletion


async def send_combined_and_delete(chat_id, combined_text):
    """Send the combined message and delete all messages in the chat after DELETE_DELAY"""
    
    send_url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"
    delete_url = f"https://tapi.bale.ai/bot{TOKEN}/deleteMessage"
    
    # send combined message
    response = requests.post(send_url, json={"chat_id": chat_id, "text": combined_text}).json()
    
    if not response.get("ok"):
        return  # if sending fails, silently return
    
    await asyncio.sleep(DELETE_DELAY)
    
    # get all messages in the chat (bot + user)
    updates = requests.get(f"https://tapi.bale.ai/bot{TOKEN}/getUpdates").json()
    
    if not updates.get("ok"):
        return
    
    message_ids = []
    
    for update in updates["result"]:
        msg = update.get("message")
        if msg and msg.get("chat", {}).get("id") == chat_id:
            message_ids.append(msg.get("message_id"))
    
    # delete all messages at once
    for msg_id in message_ids:
        requests.post(delete_url, json={"chat_id": chat_id, "message_id": msg_id})


async def get_last_30_messages(channel):
    """Fetch last 30 Telegram messages and combine them into one string"""
    try:
        messages = await client.get_messages(channel, limit=30)
        if not messages:
            return None
        combined_text = ""
        for i, msg in enumerate(reversed(messages), start=1):
            text = msg.text if msg.text else "Media post (no text)"
            combined_text += f"{i}) {text}\n\n-----------------\n\n"
        return combined_text
    except:
        return None  # silently ignore errors


async def check_bale_messages():
    """Check Bale updates and handle new commands"""
    global last_update_id
    url = f"https://tapi.bale.ai/bot{TOKEN}/getUpdates"
    params = {}
    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(url, params=params).json()
    
    if not response.get("ok"):
        return
    
    for update in response["result"]:
        last_update_id = update["update_id"]
        msg = update.get("message")
        if not msg:
            continue
        chat_id = msg.get("chat", {}).get("id")
        text = msg.get("text", "").strip()
        if not chat_id or not text:
            continue
        
        # treat the message as a Telegram channel username
        combined_posts = await get_last_30_messages(text)
        if combined_posts:
            await send_combined_and_delete(chat_id, combined_posts)
        # silently ignore if invalid channel


async def main():
    while True:
        try:
            await check_bale_messages()
        except:
            pass  # silently ignore all errors
        await asyncio.sleep(3)  # check every 3 seconds


with client:
    client.loop.run_until_complete(main())

