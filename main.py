# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
import base64

# 🟢 Base64 से 'credentials.json' बनाना और Private Key ऑटो-फिक्स करना
b64_creds = os.getenv('GOOGLE_JSON_BASE64') or os.getenv('GOOGLE_JSON')

if b64_creds:
    try:
        # Base64 डिकोड का प्रयास करें (अगर Base64 में है)
        try:
            decoded_text = base64.b64decode(b64_creds).decode('utf-8')
            info = json.loads(decoded_text)
        except Exception:
            # अगर नॉर्मल JSON स्ट्रिंग है
            info = json.loads(b64_creds)

        # 🔧 Private Key के PEM फ़ॉर्मैट की गहरी मरम्मत
        if "private_key" in info:
            pk = info["private_key"]
            pk = pk.replace('\\n', '\n').replace('\r', '')
            
            # यदि Newlines पूरी तरह गायब होकर एक लाइन में आ गई हों
            if "-----BEGIN PRIVATE KEY-----" in pk:
                body = pk.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()
                # स्पेस या टूटे कैरेक्टर्स हटाकर क्लीन की बॉडी बनाना
                body = body.replace(" ", "\n")
                pk = f"-----BEGIN PRIVATE KEY-----\n{body}\n-----END PRIVATE KEY-----\n"
            
            info["private_key"] = pk

        # फ़ाइल लिखना
        with open('credentials.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2)

        print("✅ credentials.json generated & PEM format repaired!")

    except Exception as e:
        print(f"❌ Error repairing credentials.json: {e}")

# 🟢 मॉड्युल्स इम्पोर्ट
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
            "status": "success",
            "reply": "नमस्ते! आपका संदेश मिल गया है। कृपया अपना प्रश्न पूछें।",
            "response": "नमस्ते! आपका संदेश मिल गया है। कृपया अपना प्रश्न पूछें।"
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
