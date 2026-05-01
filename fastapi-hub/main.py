from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import threading
import os

app = FastAPI()
load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def send_to_discord(message: str):
    try:
        print("➡️ Sending to Discord...")
        res = requests.post(
            DISCORD_WEBHOOK,
            json={"content": message},
            timeout=5
        )
        print(f"✅ Discord response: {res.status_code}")
    except Exception as e:
        print("❌ Error sending to Discord:", e)

def send_async(message: str):
    thread = threading.Thread(target=send_to_discord, args=(message,))
    thread.start()

@app.post("/event")
async def receive_event(request: Request):
    print("🔥 Received request")

    payload = await request.json()
    print("📦 Payload:", payload)

    app_name = payload.get("app", "unknown")
    level = payload.get("level", "info")
    message = payload.get("message", "")
    
    if level == "error":
        formatted = f"❌ [{level.upper()}] ({app_name}) {message}"
    elif level == "warning":
        formatted = f"⚠️ [{level.upper()}] ({app_name}) {message}"
    else:
        formatted = f"ℹ️ [{level.upper()}] ({app_name}) {message}"

    send_async(formatted)

    print("🚀 Returning response")
    return {"status": "ok"}