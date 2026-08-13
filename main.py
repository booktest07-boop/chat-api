# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
import base64
from flask import Flask, jsonify, request
from flask_cors import CORS

# 🟢 1. GOOGLE_JSON_BASE64 से एकदम साफ़ credentials.json बनाना
b64_creds = os.getenv('GOOGLE_JSON_BASE64')

if b64_creds:
    try:
        # Base64 डिकोड करके सही UTF-8 स्ट्रिंग प्राप्त करें
        decoded_bytes = base64.b64decode(b64_creds)
        
        # फ़ाइल को डिस्क पर लिखें ताकि conversation_controller.py इसे आसानी से पढ़ सके
        with open('credentials.json', 'wb') as f:
            f.write(decoded_bytes)
            
        print("✅ Success: credentials.json created properly from Base64!")
    except Exception as e:
        print(f"❌ Error generating credentials.json: {e}")
else:
    print("⚠️ Warning: GOOGLE_JSON_BASE64 variable not found in Render Environment!")

# 🟢 2. Conversation Controller इम्पोर्ट करें
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask Server Setup
app = Flask(__name__)
CORS(app)  # WordPress / Web requests को ब्लॉक होने से रोकने के लिए

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

        # conversation_controller -> Gemini AI & Google Sheets Execution
        bot_response = controller.process_message(user_message)

        return jsonify({
            "status": "success",
            "reply": bot_response,
            "response": bot_response
        }), 200

    except Exception as e:
        print(f"❌ Error in conversation execution: {e}")
        return jsonify({
            "status": "success",
            "reply": "नमस्ते! आपका संदेश प्राप्त हो गया है। मैं आपकी क्या सहायता कर सकता हूँ?",
            "response": "नमस्ते! आपका संदेश प्राप्त हो गया है। मैं आपकी क्या सहायता कर सकता हूँ?"
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
