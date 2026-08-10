# ========================================================
# MAIN APPLICATION ENGINE - LPAI PLATFORM
# ========================================================

import sys
import time
from flask import Flask, jsonify, request
from conversation_controller import ConversationController, INSTITUTE_NAME, FOUNDER_NAME

# Flask Web Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "platform": INSTITUTE_NAME,
        "founder": FOUNDER_NAME,
        "message": "LPAI Platform API is Live!"
    })

def run_chat_simulation(controller):
    """
    टर्मिनल पर AI एजेंट के साथ लाइव मैनुअल चैट
    """
    print("=" * 60)
    print(f"🤖 Welcome to {INSTITUTE_NAME} AI Career Guide!")
    print(f"    Platform: LPAI | Founder: {FOUNDER_NAME}")
    print("=" * 60)
    print("Commands:")
    print("  • Type '/summary' to view current student profile summary.")
    print("  • Type '/reset'   to start a new student session.")
    print("  • Type 'exit', 'quit' or '/exit' to quit the application.")
    print("=" * 60 + "\n")

    # Initial Welcome Message
    initial_response = controller.process_message("")
    print(f"🤖 AI Agent:\n{initial_response}\n")

    while True:
        try:
            user_input = input("👤 You: ").strip()

            if user_input.lower() in ["exit", "/exit", "quit", "/quit", "bye"]:
                print(f"\n🤖 AI Agent:\nधन्यवाद **{controller.student.name if controller.student.name else 'जी'}**! {INSTITUTE_NAME} से जुड़ने के लिए आपका आभार। आपका दिन शुभ हो! 🙏\n")
                print("👋 Exiting LPAI Application. Good luck!")
                break
            
            elif user_input.lower() in ["/reset", "reset"]:
                controller.reset_conversation()
                print("\n🔄 Conversation reset successfully!\n")
                welcome_msg = controller.process_message("")
                print(f"🤖 AI Agent:\n{welcome_msg}\n")
                continue

            elif user_input.lower() in ["/summary", "summary"]:
                summary = controller.format_student_summary()
                print(f"\n{summary}\n")
                continue

            if not user_input:
                continue

            response = controller.process_message(user_input)
            print(f"\n🤖 AI Agent:\n{response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Application terminated by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️ An error occurred: {e}\n")

def run_full_automated_test(controller):
    print("\n" + "=" * 60)
    print("🧪 FULL AUTOMATED CONVERSATION TEST MODE")
    print("=" * 60 + "\n")

    test_sequence = [
        "",                     # Welcome Message Trigger
        "Mohan Lal",            # Name
        "Job",                  # Career Goal
        "Digital Marketer",     # Job Profile
        "B.Com",                # Qualification
        "Basic Knowledge hai",  # Computer Knowledge
        "Offline",              # Mode
        "Syllabus bataye",      # Syllabus Query
        "Classes kitne ghante ki hoti hai?", # Timing Query
        "Fees kitni hai?",      # Fees Query
        "Fees bahut jyada hai kam karo", # Fees Objection
        "Haan demo book kar do",# Demo Decision
        "Morning Batch",        # Batch Slot
        "Kal aaunga",           # Demo Date
        "9876543210",           # 📱 Mobile Number
        "Center address kahan hai?", # Address Query
        "Haan admission confirm kar do" # Admission Confirmation
    ]

    for step, student_msg in enumerate(test_sequence):
        if student_msg:
            print(f"👤 Student: {student_msg}")
        
        response = controller.process_message(student_msg)
        print(f"🤖 AI Agent:\n{response}\n")
        print("-" * 60)

    print("\n✅ FULL TEST COMPLETED SUCCESSFULLY!\n")
    print(controller.format_student_summary())
    print("=" * 60)

def test_youtube_moderation(controller):
    """
    यूट्यूब कमेंट मॉडरेशन टेस्ट
    """
    print("\n" + "=" * 60)
    print("📌 YOUTUBE COMMENT MODERATION TESTER")
    print("=" * 60)

    sample_comments = [
        "Sir ADCA course ki fees kitni hai?",
        "Yeh sab bakwas hai aur fake video hai",
        "Very nice video sir, thanks for explaining Tally Prime",
        "Aapka center kahan hai location bataye?",
        "Faltu bakwas mat karo gaali mat do"
    ]

    for idx, comment in enumerate(sample_comments, 1):
        print(f"\nComment #{idx}: \"{comment}\"")
        result = controller.check_youtube_comment_moderation(comment)
        print(f"  └─ Action: {result['action']}")
        print(f"  └─ Reason: {result['reason']}")
        if result['reply']:
            print(f"  └─ Auto-Reply:\n{result['reply']}")
    print("=" * 60 + "\n")

def main():
    controller = ConversationController()

    print("\nSelect Mode:")
    print("1️⃣ Run Interactive AI Career Counselor Chat (Manual)")
    print("2️⃣ Run Full Automated Conversation Test (Auto All Steps)")
    print("3️⃣ Run YouTube Comment Moderation Test")
    print("4️⃣ Exit")

    choice = input("\nEnter choice (1/2/3/4): ").strip()

    if choice == "1":
        run_chat_simulation(controller)
    elif choice == "2":
        run_full_automated_test(controller)
    elif choice == "3":
        test_youtube_moderation(controller)
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Starting Interactive Chat by default...\n")
        run_chat_simulation(controller)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
