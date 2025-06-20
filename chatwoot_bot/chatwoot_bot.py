from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)  # ✅ define app first

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return '✅ Chatwoot Bot is Live'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('content')

    if not message:
        return jsonify({"content": "No message received."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"content": reply})

    except Exception as e:
        return jsonify({"content": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

