from flask import Flask, request, jsonify
from flask_cors import CORS

from conversation_controller import ConversationController


app = Flask(__name__)
CORS(app)

# आपका Existing AI Career Counsellor Brain
controller = ConversationController()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_msg = data.get("message", "").strip()

    # Website से नई conversation शुरू होने पर
    if user_msg == "START_CONVERSATION":
        response = (
            "🙏 नमस्ते Learning Point Destination में आपका हार्दिक स्वागत है।\n\n"
            "क्या मैं आपका नाम जान सकता हूँ?"
        )

        return jsonify({"response": response})

    # Student का message आपके Existing ConversationController को भेजना
    response = controller.process_message(user_msg)

    return jsonify({"response": response})


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Learning Point Destination AI Career Counsellor API is running."
    })


if __name__ == "__main__":
    app.run()
