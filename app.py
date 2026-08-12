from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_msg = data.get("message", "")
    
    if user_msg == "START_CONVERSATION":
        return jsonify({"response": "🙏 नमस्ते Learning Point Destination में आपका हार्दिक स्वागत है। क्या मैं आपका नाम जान सकता हूँ?"})
    
    reply_text = f"नमस्ते! Learning Point Destination AI Counsellor में आपका स्वागत है। आपने लिखा: '{user_msg}'"
    return jsonify({"response": reply_text})

if __name__ == '__main__':
    app.run()