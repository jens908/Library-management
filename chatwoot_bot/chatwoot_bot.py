from flask import Flask, request
import openai
import os
import requests

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
CHATWOOT_API_URL = "https://app.chatwoot.com"  # or your Chatwoot domain
CHATWOOT_TOKEN = os.environ.get("CHATWOOT_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("content")
    conversation_id = data.get("conversation", {}).get("id")

    if not message or not conversation_id:
        return {"status": "ignored"}, 200

    # OpenAI reply
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
    )
    reply = completion.choices[0].message.content

    # Reply back to Chatwoot
    requests.post(
        f"{CHATWOOT_API_URL}/api/v1/conversations/{conversation_id}/messages",
        headers={
            "Content-Type": "application/json",
            "api_access_token": CHATWOOT_TOKEN
        },
        json={
            "content": reply,
            "message_type": "outgoing"
        },
    )

    return {"status": "ok"}, 200

# ✅ Add this to start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
