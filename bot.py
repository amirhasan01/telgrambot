import requests

TOKEN = "1934568871:UAzs_KGSXXi8sZ-e8OdNVBLhko2cc0apn4E"
CHAT_ID = 650686292  # replace with the id from getUpdates

url = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "Hello from my Python bot!"
}

response = requests.post(url, json=data)
print(response.text)
