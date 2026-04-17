import time
import requests
import re

FASTAPI_URL = "http://localhost:8000/event" #URL of FastAPI Hub
LOG_FILE = "E:\\NAS\\telegrambot\\logs\\bot.log" #Log file locaiton


def send_event(level, message):
    payload = {
        "app": "telegram-bot",
        "level": level,
        "message": message.strip()
    }

    try:
        requests.post(FASTAPI_URL, json=payload, timeout=3)
    except Exception as e:
        print("❌ send error:", e)


def follow_log(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(0, 2)  # 👉 Read last line

        while True:
            line = f.readline()

            if not line:
                time.sleep(1)
                continue

            print("📄", line.strip())
                
            line_lower = line.lower()

            # Notification logic
            if "queued" in line_lower:
                send_event("info", line)
            elif "queue" in line_lower:
                send_event("info", line)
            elif "conn" in line_lower:
                send_event("warning", line)
            elif "error" in line:
                send_event("error", line)

if __name__ == "__main__":
    follow_log(LOG_FILE)