import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # WordPress से कनेक्शन ब्लॉक न होने के लिए

# Controller क्लास इम्पोर्ट करना
try:
    from conversation_controller import ConversationController
    print("✅ ConversationController class loaded successfully!")
except Exception as e:
    print(f"⚠️ Controller loading error: {e}")
    ConversationController = None

# हर यूजर / सेशन के लिए अलग मेमोरी (Multi-Session Storage)
user_sessions = {}

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({
        "status": "online",
        "service": "Learning Point AI Counsellor",
        "ready": True
    }), 200

@app.route('/chat', methods=['POST', 'OPTIONS'])
@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    # CORS प्री-फ़्लाइट रिक्वेस्ट हैंडल करना
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default_user')

        # 🟢 1. अगर START_CONVERSATION आया है -> नया सेशन बनाएं और सिर्फ 1 बार वेलकम भेजें
        if user_message == "START_CONVERSATION":
            if ConversationController:
                user_sessions[session_id] = ConversationController()
            
            reply = (
                "🙏 **नमस्ते! Learning Point Destination में आपका स्वागत है।**\n\n"
                "मैं आपका 24x7 **AI Career Counsellor** हूँ। 🎯\n\n"
                "आपकी **Qualification और Goals** के अनुसार आपके लिए Best Job-Oriented Course चुनने में मैं आपकी पूरी सहायता करूँगा, ताकि आपके लिए Career के बेहतरीन रास्ते खुल सकें।\n\n"
                "शुरुआत करने के लिए, **क्या मैं आपका शुभ Name जान सकता हूँ?** 😊"
            )
            return jsonify({
                "status": "success",
                "reply": reply,
                "response": reply
            }), 200

        # 🟢 2. अगर किसी वजह से सेशन मौजूद नहीं है, तो फ्रेश सेशन बनाएं
        if session_id not in user_sessions:
            if ConversationController:
                user_sessions[session_id] = ConversationController()

        # 🟢 3. हर सामान्य मैसेज सीधा कंट्रोलर प्रोसेस करेगा (नो डुप्लीकेट वेलकम)
        controller = user_sessions.get(session_id)
        if controller:
            bot_reply = controller.process_message(user_message)
        else:
            bot_reply = "नमस्ते! कृपया अपना प्रश्न या मोबाइल नंबर साझा करें।"

        return jsonify({
            "status": "success",
            "reply": bot_reply,
            "response": bot_reply
        }), 200
        except Exception as e:
        print(f"❌ Chat processing error: {e}")
        fallback_reply = "धन्यवाद! कृपया अपना मोबाइल नंबर या कोर्स से संबंधित प्रश्न साझा करें।"
        return jsonify({
            "status": "success",
            "reply": fallback_reply,
            "response": fallback_reply
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
