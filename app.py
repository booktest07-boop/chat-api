import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # WordPress से कनेक्शन ब्लॉक न होने के लिए

# Controller को सुरक्षित लोड करना
try:
    from conversation_controller import ConversationController
    controller = ConversationController()
    print("✅ Controller loaded successfully!")
except Exception as e:
    print(f"⚠️ Controller loading error: {e}")
    controller = None

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
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get('message', '').strip()

        # अगर बोट का स्वागत संदेश चाहिए
        if user_message == "START_CONVERSATION" or not user_message:
            reply = "नमस्ते! 😊\n\n**Learning Point Destination** में आपका स्वागत है। मैं आपका AI Career Guide हूँ।\n\nक्या मैं आपका Name जान सकता हूँ?"
            return jsonify({"status": "success", "reply": reply, "response": reply}), 200

        # अगर Controller सही काम कर रहा है
        if controller:
            bot_reply = controller.process_message(user_message)
        else:
            bot_reply = "नमस्ते! आपका संदेश प्राप्त हो गया है। कृपया अपना प्रश्न पूछें।"

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
