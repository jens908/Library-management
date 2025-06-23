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

    if not message or not conversation_id:
        return {"status": "ignored"}, 200

    # Mock reply instead of OpenAI
    reply = f"Echo: {message}"

    # Reply back to Chatwoot
    requests.post(
        f"{CHATWOOT_API_URL}/api/v1/conversations/{conversation_id}/messages",
        headers={"Content-Type": "application/json", "api_access_token": CHATWOOT_TOKEN},
        json={"content": reply, "message_type": "outgoing"},
    )

    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)

