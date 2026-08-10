# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import os
import sys
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# Google Authentication In-Memory
import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet_client():
    creds_raw = os.getenv('GOOGLE_JSON')
    if not creds_raw:
        print("❌ Error: GOOGLE_JSON Environment Variable not found!")
        return None
    try:
        # JSON लोड करना
        info = json.loads(creds_raw)
        
        # Private Key की न्यू-लाइन्स (newlines) की सख्त मरम्मत
        if "private_key" in info:
            key = info["private_key"]
            key = key.replace('\\n', '\n').replace('\r', '')
            info["private_key"] = key

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # बिना फाइल बनाए सीधे Memory से Credentials लोड करना
        credentials = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(credentials)
        print("✅ Google Sheets Connected Successfully!")
        return client
    except Exception as e:
        print(f"❌ Google Sheets Connection Error: {e}")
        return None

# Google Sheet टेस्ट कनेक्शन
sheet_client = get_google_sheet_client()

from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask Web Server Setup
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
