import time
import requests
import yaml
import os
import re

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/event")
CONFIG_PATH = "/app/config.yaml"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
        
def send_event(app, level, message):
    payload = {
        "app": app,
        "level": level,
        "message": message.strip()
    }

    try:
        requests.post(FASTAPI_URL, json=payload, timeout=3)
    except Exception as e:
        print("❌ send error:", e)
        
def match_rule(line, rule):
    line_lower = line.lower()
    
    if "patterns" in rule:
        return all(p.lower() in line_lower for p in rule["patterns"])

    if "any_patterns" in rule:
        return any(p.lower() in line_lower for p in rule["any_patterns"])

    return False

def follow_file(target):
    file_path = target["file"]
    app_name = target["app"]
    rules = target.get("rules", [])

    print(f"📡 Start watching {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.seek(0, 2)  # tail mode

            while True:
                line = f.readline()

                if not line:
                    time.sleep(1)
                    continue

                print(f"[{app_name}] {line.strip()}")

                for rule in rules:
                    if match_rule(line, rule):
                        send_event(app_name, rule["level"], line)
                        break

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")

def main():
    config = load_config()
    targets = config.get("targets", [])

    for target in targets:
        import threading
        t = threading.Thread(target=follow_file, args=(target,))
        t.daemon = True
        t.start()

    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()