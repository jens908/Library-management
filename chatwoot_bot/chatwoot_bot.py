from flask import Flask, request
import os
import requests

app = Flask(__name__)

CHATWOOT_API_URL = "https://app.chatwoot.com"
CHATWOOT_TOKEN = os.environ.get("CHATWOOT_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("content")
    conversation_id = data.get("conversation", {}).get("id")
    account_id = data.get("account", {}).get("id")

    print("📥 Incoming Data:", data)
    print("🧾 Message:", message)
    print("🆔 Conversation ID:", conversation_id)
    print("🏢 Account ID:", account_id)

    if not message or not conversation_id or not account_id:
        print("⚠️ Missing required data")
        return {"status": "ignored"}, 200

    reply = f"Echo: {message}"

    response = requests.post(
        f"{CHATWOOT_API_URL}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages",
        headers={"Content-Type": "application/json", "api_access_token": CHATWOOT_TOKEN},
        json={"content": reply, "message_type": "outgoing"},
    )

    print("📤 Sending reply to Chatwoot...")
    print("🔗 URL:", f"{CHATWOOT_API_URL}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages")
    print("📦 Payload:", {"content": reply, "message_type": "outgoing"})
    print("📡 Response:", response.status_code, response.text)

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)

