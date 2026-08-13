# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
import base64
from flask import Flask, jsonify, request
from flask_cors import CORS

# 🟢 Base64 से credentials.json फाइल बनाना
b64_creds = os.getenv('GOOGLE_JSON_BASE64')

if b64_creds:
    try:
        decoded_bytes = base64.b64decode(b64_creds)
        with open('credentials.json', 'wb') as f:
            f.write(decoded_bytes)
        print("✅ Success: credentials.json created properly from Base64!")
    except Exception as e:
        print(f"❌ Error generating credentials.json: {e}")
else:
    print("⚠️ GOOGLE_JSON_BASE64 variable not found!")

# 🟢 Conversation Controller इंपोर्ट
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

app = Flask(__name__)
CORS(app)  # WordPress से कनेक्ट होने की अनुमति देता है

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
        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get('message', '').strip()

        bot_response = controller.process_message(user_message)

        return jsonify({
            "status": "success",
            "reply": bot_response,
            "response": bot_response
        }), 200

    except Exception as e:
        print(f"❌ Error in chat handler: {e}")
        return jsonify({
            "status": "success",
            "reply": "नमस्ते! आपका संदेश मिल गया है। कृपया अपना सवाल पूछें।",
            "response": "नमस्ते! आपका संदेश मिल गया है। कृपया अपना सवाल पूछें।"
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
