# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import sys
import time
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# 🟢 Render के Environment Variable से credentials.json बनाना
if not os.path.exists('credentials.json'):
    creds_data = os.getenv('GOOGLE_JSON')
    if creds_data:
        with open('credentials.json', 'w') as f:
            f.write(creds_data)
        print("Successfully created credentials.json from Environment Variable")

# Flask Web Server Setup
app = Flask(__name__)
CORS(app)

# Single Global Controller Instance
controller = ConversationController()

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "platform": INSTITUTE_NAME,
        "founder": FOUNDER_NAME,
        "message": "LPAI Platform API is Live!"
    })

@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()

        bot_response = controller.process_message(user_message)

        return jsonify({
            "status": "success",
            "reply": bot_response,
            "response": bot_response
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
