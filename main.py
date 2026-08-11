# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# 1. Google Credentials in-memory setup
import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet_client():
    creds_raw = os.getenv('GOOGLE_JSON')
    if not creds_raw:
        return None
    try:
        info = json.loads(creds_raw)
        if "private_key" in info:
            info["private_key"] = info["private_key"].replace('\\n', '\n').replace('\r', '')

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(credentials)
        print("✅ Google Sheets Connected Successfully!")
        return client
    except Exception as e:
        print(f"⚠️ Google Sheets Connection Warning: {e}")
        return None

# Initial Sheet Client Check
sheet_client = get_google_sheet_client()

# 2. Importing ConversationController (आपकी मुख्य फाइल)
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
        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get('message', '').strip()

        # 🟢 मुख्य कनेक्शन: यहाँ बातचीत ConversationController से ही हैंडल हो रही है
        bot_response = controller.process_message(user_message)

        return jsonify({
            "status": "success",
            "success": True,
            "reply": bot_response,
            "response": bot_response
        }), 200

    except Exception as e:
        # अगर controller में कोई भी दिक्कत आती है तो Render के logs में दिखेगा
        print(f"❌ Error inside ConversationController: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
