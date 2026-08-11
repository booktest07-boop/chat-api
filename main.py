# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
import base64

# 🟢 Base64 कोड को डिकोड करके असली credentials.json फाइल बनाना
b64_creds = os.getenv('GOOGLE_JSON_BASE64')
if b64_creds:
    try:
        # Base64 को वापस ओरिजिनल JSON स्ट्रिंग में बदलें
        decoded_bytes = base64.b64decode(b64_creds)
        
        # credentials.json फाइल बनाएं
        with open('credentials.json', 'wb') as f:
            f.write(decoded_bytes)
            
        print("✅ credentials.json successfully generated from Base64!")
    except Exception as e:
        print(f"❌ Error decoding GOOGLE_JSON_BASE64: {e}")
else:
    print("⚠️ GOOGLE_JSON_BASE64 variable not found!")

# 🟢 अब आपके सभी Modules और Controllers लोड होंगे
from flask import Flask, jsonify, request
from flask_cors import CORS
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

app = Flask(__name__)
CORS(app)

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
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
