# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json

# 🟢 स्टेप 1: किसी भी मॉड्यूल के लोड होने से पहले 'credentials.json' फ़ाइल बनाएं
creds_raw = os.getenv('GOOGLE_JSON')
if creds_raw:
    try:
        # JSON लोड करें
        info = json.loads(creds_raw)
        
        # Private Key की सभी गलत लाइनों और एक्स्ट्रा सिम्बल्स को क्लीन करें
        if "private_key" in info:
            key = info["private_key"]
            # अगर \n स्ट्रिंग के रूप में है तो उसे असली Newline से रिप्लेस करें
            key = key.replace('\\n', '\n').replace('\r', '')
            info["private_key"] = key

        # अब सही JSON को credentials.json फ़ाइल में लिख दें
        with open('credentials.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2)
            
        print("✅ Successfully created clean credentials.json file!")
    except Exception as e:
        print(f"❌ Error writing credentials.json: {e}")
else:
    print("⚠️ GOOGLE_JSON variable not found in Render Environment!")

# 🟢 स्टेप 2: अब बाकी के मॉड्युल्स इम्पोर्ट करें (अब conversation_controller को फाइल मिल जाएगी)
from flask import Flask, jsonify, request
from flask_cors import CORS
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask App Setup
app = Flask(__name__)
CORS(app)

# Controller Instance
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

        # Conversation Controller से AI रिस्पॉन्स लें
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
