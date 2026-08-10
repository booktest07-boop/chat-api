# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import time
import json

# 1. सबसे पहले Credentials फाइल बनाएं (किसी भी अन्य इंपोर्ट से पहले)
creds_data = os.getenv('GOOGLE_JSON')
if creds_data and not os.path.exists('credentials.json'):
    try:
        # JSON स्ट्रिंग को सही फॉर्मेट में लोड और सेव करें
        parsed_json = json.loads(creds_data)
        with open('credentials.json', 'w') as f:
            json.dump(parsed_json, f, indent=2)
        print("✅ Successfully generated credentials.json from Environment Variable!")
    except Exception as e:
        print(f"⚠️ Error creating credentials.json: {e}")

# 2. अब बाकी Modules और Controller इंपोर्ट करें
from flask import Flask, jsonify, request
from flask_cors import CORS
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask App Setup
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
