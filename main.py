# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM (WEB API MODE)
# ========================================================

import sys
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask Web Server Setup
app = Flask(__name__)
CORS(app)  # वेबसाइट से कनेक्शन (CORS) allow करने के लिए

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

# 🟢 यह API आपकी वेबसाइट के चैट विजेट के साथ बात करेगी
@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()

        # Conversation Controller से AI रिस्पॉन्स प्राप्त करें
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
