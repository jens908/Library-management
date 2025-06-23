from flask import Flask, request
import os
import requests

app = Flask(__name__)

CHATWOOT_API_URL = "https://app.chatwoot.com"
CHATWOOT_TOKEN = os.environ.get("CHATWOOT_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📥 Incoming Data:", data)

    message = data.get("content")
    conversation_id = data.get("conversation", {}).get("id")
    print(f"🧾 Message: {message}")
    print(f"🆔 Conversation ID: {conversation_id}")

    if not message or not conversation_id:
        print("⚠️ Missing message or conversation ID")
        return {"status": "ignored"}, 200

    reply = f"Echo: {message}"

    url = f"{CHATWOOT_API_URL}/api/v1/conversations/{conversation_id}/messages"
    headers = {
        "Content-Type": "application/json",
        "api_access_token": CHATWOOT_TOKEN
    }
    payload = {
        "content": reply,
        "message_type": "outgoing"
    }

    print("📤 Sending reply to Chatwoot...")
    print("🔗 URL:", url)
    print("📦 Payload:", payload)

    response = requests.post(url, headers=headers, json=payload)
    print("📡 Response:", response.status_code, response.text)

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)

