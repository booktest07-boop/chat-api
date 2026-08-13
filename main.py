# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM (FINAL ENGINE)
# ========================================================

import os
import sys
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# 🟢 1. GOOGLE_JSON से credentials.json फाइल बनाना
creds_raw = os.getenv('GOOGLE_JSON')

if creds_raw:
    try:
        # JSON लोड करें
        info = json.loads(creds_raw)
        
        # अगर \n में दिक्कत हो तो उसे सही करें
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace('\\n', '\n').replace('\r', '')

        with open('credentials.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2)
            
        print("✅ Success: credentials.json created successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Could not parse GOOGLE_JSON: {e}")
else:
    print("⚠️ GOOGLE_JSON variable not set. Running in standard mode.")

# 🟢 2. Conversation Controller इंपोर्ट करें
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask Server Setup
app = Flask(__name__)
CORS(app)  # WordPress से सुरक्षित कनेक्शन के लिए

# Single Controller Instance
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

        # Conversation Controller -> Gemini AI से जवाब लाना
        bot_response = controller.process_message(user_message)

        return jsonify({
            "status": "success",
            "reply": bot_response,
            "response": bot_response
        }), 200

    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        return jsonify({
            "status": "success",
            "reply": "नमस्ते! आपका संदेश प्राप्त हो गया है। कृपया अपना प्रश्न पूछें।",
            "response": "नमस्ते! आपका संदेश प्राप्त हो गया है। कृपया अपना प्रश्न पूछें।"
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
