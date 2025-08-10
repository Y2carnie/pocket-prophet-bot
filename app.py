import os
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_PATH = f"/webhook/{TELEGRAM_TOKEN}"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = FastAPI()

class Update(BaseModel):
    update_id: int
    message: dict = None
    edited_message: dict = None

@app.get("/")
def home():
    return {"status": "Pocket Prophet bot is alive"}

@app.post(WEBHOOK_PATH)
async def process_webhook(update: Update):
    message = update.message or update.edited_message
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    user_text = message.get("text", "")

    # Example reply (later we can hook to OpenAI)
    reply_text = f"🔮 Pocket Prophet says: You asked - '{user_text}'"

    send_message(chat_id, reply_text)
    return {"ok": True}

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)
