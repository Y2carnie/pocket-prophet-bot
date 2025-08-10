import os
from fastapi import FastAPI, Request
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Webhook route — matches your bot token exactly
@app.post(f"/webhook/{TELEGRAM_BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()

    # Extract message
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # Here you can add your OpenAI logic or a simple reply
        reply = f"You said: {user_message}"

        # Send reply to Telegram
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}

@app.get("/")
def home():
    return {"status": "Bot is running!"}
