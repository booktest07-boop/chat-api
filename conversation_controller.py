# ==================================================
# Google Sheet Connection Setup (Using Direct URL)
# ========================================================
try:
    import os
    import base64
    import json
    import gspread

    raw_env_data = os.environ.get("GOOGLE_JSON_BASE64", "").strip()

    if not raw_env_data:
        raise ValueError("GOOGLE_JSON_BASE64 environment variable not found")

    # 1. अगर वैल्यू सीधे JSON है
    if raw_env_data.startswith("{"):
        credentials_info = json.loads(raw_env_data)
    else:
        # 2. अगर Base64 है
        cleaned_b64 = "".join(raw_env_data.split())
        missing_padding = len(cleaned_b64) % 4
        if missing_padding:
            cleaned_b64 += "=" * (4 - missing_padding)

        decoded_bytes = base64.b64decode(cleaned_b64)
        credentials_info = json.loads(decoded_bytes.decode("utf-8", errors="ignore"))

    if "private_key" in credentials_info:
        credentials_info["private_key"] = credentials_info["private_key"].replace("\\n", "\n")

    # Google Auth
    gc = gspread.service_account_from_dict(credentials_info)

    # 🟢 यहाँ आपकी पूरी Google Sheet की URL से सीधा कनेक्शन
    sheet_url = "https://docs.google.com/spreadsheets/d/143BX78uGM-IeHPx-bYQQhkswaiOf1Zn-eRLpz5dY5IY/edit?gid=0#gid=0"
    spreadsheet = gc.open_by_url(sheet_url)
    sheet = spreadsheet.sheet1

    print("✅ Google Sheet Connected Successfully via URL!")

except Exception as e:
    print(f"❌ Google Sheets Connection Error: {e}")
    sheet = None
    
# ========================================================
# SECTION 02 : COURSE CONSTANTS (Learning Point Destination)
# ========================================================

INSTITUTE_NAME = "Learning Point Destination"
FOUNDER_NAME = "Ramlakhan Rathor"
PROJECT_NAME = "LPAI Platform"
VERSION = "1.0"

# संस्था के सभी 31 उपलब्ध कोर्सेस (Complete Updated List)
COURSES_DATA = {
    # Basic & Fundamental
    "BASIC": {"name": "Basic Computer"},
    "CCC": {"name": "CCC (Course on Computer Concepts)"},
    "OFFICE": {"name": "MS Office"},
    "INTERNET": {"name": "Internet & Email"},
    "DATA_ENTRY": {"name": "Data Entry Operator"},
    "OFFICE_AUTO": {"name": "Office Automation Course"},

    # Diplomas & Professional Programs
    "ADCA": {"name": "ADCA (Advanced Diploma in Computer Applications)"},
    "JOB_ORIENTED": {"name": "Job-Oriented Computer Course"},
    "TEACHER_TRG": {"name": "Computer Teacher Training"},

    # Accounting & Finance
    "TALLY": {"name": "Tally Prime with GST"},
    "BUSY": {"name": "Busy Accounting Software"},
    "EXCEL_ADV": {"name": "Advanced Excel"},
    "PRO_ACCT": {"name": "Professional Accounting Course"},

    # Design, Media & Content
    "GRAPHIC": {"name": "Graphic Designing"},
    "DTP": {"name": "DTP (Desktop Publishing)"},
    "CANVA": {"name": "Canva Designing"},
    "VIDEO_EDIT": {"name": "Video Editing"},

    # Digital Marketing & Web
    "DIGITAL_MKTG": {"name": "Digital Marketing"},
    "WEB_DESIGN": {"name": "Web Designing"},
    "SEO": {"name": "SEO (Search Engine Optimization)"},
    "SMM": {"name": "Social Media Marketing"},
    "WORDPRESS": {"name": "WordPress Website Development"},
    "ECOMMERCE": {"name": "E-Commerce Management"},

    # Modern Tech, Data & AI
    "PYTHON": {"name": "Python Programming"},
    "POWER_BI": {"name": "Power BI"},
    "AI_TOOLS": {"name": "AI Tools for Productivity"},
    "FREELANCING": {"name": "Freelancing Skills"},

    # Soft Skills & Career Development
    "SPOKEN_ENG": {"name": "Spoken English"},
    "PERSONALITY": {"name": "Personality Development"},
    "INTERVIEW_PREP": {"name": "Interview Preparation"},
    "RESUME_BUILD": {"name": "Resume Building"}
}
# ========================================================
# SECTION 03 : STUDENT PROFILE CLASS
# ========================================================

class StudentProfile:
    def __init__(self):
        self.name = ""
        self.phone = ""  # <--- मोबाइल नंबर का वैरिएबल
        self.career_goal = ""
        self.job_type = ""
        self.qualification = ""
        self.computer_knowledge = ""
        self.learning_mode = ""
        self.recommended_course = ""
        self.selected_time_slot = ""
        self.selected_date_time = ""
        self.demo_booked = False
        self.visit_scheduled = False
        self.admission_status = "Pending"

# ========================================================
# SECTION 04 : CONVERSATION CONTROLLER CLASS
# ========================================================

class ConversationController:

# ========================================================
# SECTION 05 : INITIALIZATION (__init__)
# ========================================================

    def __init__(self):
        # Student Profile Instance
        self.student = StudentProfile()

        # Conversation State Tracking (यहाँ "name" सेट किया गया है)
        self.current_stage = "name"
        self.previous_stage = ""
        self.session_active = True
        self.conversation_completed = False

        # Status Flags
        self.is_interested = False
        self.demo_booked = False
        self.visit_scheduled = False
        self.admission_confirmed = False

        # Memory & Preferences
        self.conversation_history = []
        self.last_asked_question = ""
        
        # YouTube Comment Moderation Keywords (डिलीट करने योग्य शब्द)
        self.forbidden_keywords = [
            "bakwas", "fake", "fraud", "faltu", "gaali", "gali", 
            "बकवास", "फेक", "फ्रॉड", "फ़ालतू", "गाली", "chutiya", "madarchod"
        ]
    # 🟢 ----------------------------------------------------
    # यहाँ पेस्ट करें: GOOGLE SHEET SAVE FUNCTION
    # ----------------------------------------------------
    def save_student_to_sheet(self):
        """Student का डेटा Google Sheet में भेजने के लिए फ़ंक्शन"""
        if sheet:
            try:
                course_key = getattr(self.student, 'recommended_course', '')
                course_obj = COURSES_DATA.get(course_key, {}) if 'COURSES_DATA' in globals() else {}
                course_name = course_obj.get('name', course_key)

                sheet.append_row([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),      # Date & Time
                    self.student.name if self.student.name else "N/A",  # Name
                    self.student.phone if self.student.phone else "N/A",# 📱 Phone Number
                    self.student.career_goal,                          # Goal
                    self.student.job_type,                            # Profile
                    self.student.qualification,                       # Qualification
                    self.student.computer_knowledge,                  # Knowledge
                    self.student.learning_mode,                      # Mode (Offline/Online)
                    course_name,                                      # Course
                    self.student.selected_time_slot,                  # Time Slot
                    self.student.selected_date_time,                  # Demo/Visit Date
                    "Yes" if self.student.demo_booked else "No",      # Demo Booked
                    self.student.admission_status                     # Status (Pending)
                ])
                print(f"🟢 Data for {self.student.name} ({self.student.phone}) successfully saved to Google Sheet!")
            except Exception as e:
                print(f"🔴 Error saving to Google Sheet: {e}")
        
    # ========================================================
    # SECTION 06 : MAIN PROCESS MESSAGE & WELCOME HANDLERS
    # ========================================================

    def clean_text(self, text):
        if not text:
            return ""
        return str(text).strip()

    def process_message(self, user_message):
        # 1. टेक्स्ट साफ़ करना
        cleaned_msg = self.clean_text(user_message)
        
        # 2. हिस्ट्री में जोड़ना
        self.conversation_history.append({"user": cleaned_msg})

       # 3. Exit Commands Check
        if cleaned_msg.lower() in ["exit", "quit", "bye", "बंद करो", "अलविदा"]:
            return "बातचीत समाप्त करने के लिए धन्यवाद! यदि आपका कोई अन्य प्रश्न हो, तो बेझिझक पूछें।"

        if not cleaned_msg and self.current_stage == "welcome":
            return self.handle_welcome()
        # 3. Completed Conversation Check
        if self.conversation_completed:
            return self.handle_completed_stage(cleaned_msg)

        # 4. DIRECT OVERRIDE FOR ADMISSION CONFIRMATION
        # अगर छात्र 'admission confirm' बोलता है तो सीधे admission decision हैंडल करें
        norm_msg = cleaned_msg.lower()
        if any(w in norm_msg for w in ["admission", "confirm", "कन्फर्म", "एडमिशन"]) and any(w in norm_msg for w in ["haan", "ha", "yes", "kar do", "कर दो", "करदो", "हाँ"]):
            self.current_stage = "admission_decision"
            return self.handle_admission_decision(cleaned_msg)

        # 5. Universal & Objection Checks
        objection_answer = None
        if objection_answer:
            return objection_answer

        universal_answer = None
        if universal_answer:
            if getattr(self.student, 'demo_booked', False):
                self.current_stage = "admission_decision"
            return universal_answer

        # 6. MAIN STAGE FLOW CONTROLLER
        if self.current_stage == "welcome":
            return self.handle_welcome()
        elif self.current_stage == "name":
            return self.handle_name(cleaned_msg)
        elif self.current_stage == "career_goal":
            return self.handle_career_goal(cleaned_msg)
        elif self.current_stage == "job_type":
            return self.handle_job_type(cleaned_msg)
        elif self.current_stage == "business_type":
            return self.handle_business_type(cleaned_msg)
        elif self.current_stage == "freelancing_skill":
            return self.handle_freelancing_skill(cleaned_msg)
        elif self.current_stage == "qualification":
            return self.handle_qualification(cleaned_msg)
        elif self.current_stage == "computer_knowledge":
            return self.handle_computer_knowledge(cleaned_msg)
        elif self.current_stage == "learning_mode":
            return self.handle_learning_mode(cleaned_msg)
        elif self.current_stage == "recommendation_response":
            return self.handle_recommendation_response(cleaned_msg)
        elif self.current_stage == "course_followup":
            return self.handle_course_followup(cleaned_msg)
        elif self.current_stage == "demo_decision":
            return self.handle_demo_decision(cleaned_msg)
        elif self.current_stage == "demo_timing":
            return self.handle_demo_timing(cleaned_msg)
        elif self.current_stage == "demo_date_time":
            return self.handle_demo_date_time_extended(cleaned_msg)
        elif self.current_stage == "ask_phone":  # <--- यह नई लाइन जोड़ें
            return self.handle_phone_submission(cleaned_msg)
        elif self.current_stage == "visit_decision":
            return self.handle_visit_decision(cleaned_msg)
        elif self.current_stage == "visit_timing":
            return self.handle_visit_timing(cleaned_msg)
        elif self.current_stage == "visit_date_time":
            return self.handle_visit_date_time_extended(cleaned_msg)
        elif self.current_stage == "admission_decision":
            return self.handle_admission_decision(cleaned_msg)

        # 7. Fallback Handler
        return self.handle_fallback(cleaned_msg)
    
       # ✅ सही तरीका (pass जोड़ दिया)
    def some_previous_function(self):
        pass
    
    def handle_welcome(self):
            self.current_stage = "name"
            return "नमस्ते! 😊\n\n**Learning Point Destination** में आपका स्वागत है। मैं आपका AI Career Guide हूँ।\n\nक्या मैं आपका Name जान सकता हूँ?"

    # ========================================================
    # SECTION 07 : CERTIFICATE & ISO VALIDITY HANDLER
    # ========================================================

    def handle_certificate_question(self):
        return (
            f"**{self.student.name if self.student.name else 'जी'}**, **{INSTITUTE_NAME}** से Course पूरा करने पर आपको **ISO Certified** और **Government Recognized** Certificate प्रदान किया जाता है। 📜\n\n"
            f"यह Certificate सभी Private Jobs, MNCs और Government Job Vacancies/Promotions के लिए **100% Valid** और मान्य है। 😊"
        )

  # ========================================================
    # SECTION 08 : NAME HANDLER
    # ========================================================

    def extract_name(self, text):
        import re
        text = text.strip()
        cleaned = re.sub(r'^(mera\s+naam|my\s+name\s+is|i\s+am|myself|main|mai|this\s+is|naam\s+hai)\s+', '', text, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+(hai|hoon|hu|he)$', '', cleaned, flags=re.IGNORECASE).strip()
        
        words = cleaned.split()
        if words and len(words) <= 4:
            return " ".join(w.capitalize() for w in words)
        return cleaned.title() if cleaned else text.title()

    def handle_name(self, text):
        extracted_name = self.extract_name(text)
        if not extracted_name or len(extracted_name) < 2:
            return "कृपया अपना सही Name बताइए ताकि हम बात आगे बढ़ा सकें।"
            
        self.student.name = extracted_name
        self.current_stage = "career_goal"
        
        response = (
            f"बहुत अच्छा **{self.student.name} जी**! 😊\n\n"
            f"आपसे मिलकर बहुत खुशी हुई।\n\n"
            f"अपने Future की Planning करना बहुत अच्छी शुरुआत है। मुझे बताइए, आप आगे चलकर किस Field में जाना चाहते हैं?\n\n"
            f"1️⃣ **Job** (अच्छी Job पाना)\n"
            f"2️⃣ **Business** (खुद का काम / Business)\n"
            f"3️⃣ **Freelancing** (घर बैठे Online काम करना)"
        )
        return response

    # ========================================================
    # SECTION 09 : CAREER GOAL HANDLER (UPDATED JOB TITLES)
    # ========================================================

    def handle_career_goal(self, text):
        norm_text = text.lower().strip()

        # 🟢 1. BUSINESS (सारे Typos, हिंदी शब्द और Own Business कीवर्ड्स)
        business_keywords = [
            "business", "busines", "bussnies", "bosinees", "bussiness", "biz",
            "khud", "own", "apna", "self", "startup", "dukan", "shop", "vyapar", "व्यापार", "बिजनेस", "2"
        ]
        
        # 🟢 2. JOB (Naukri, Work, Placement आदि)
        job_keywords = [
            "job", "jobs", "naukri", "nokri", "naukari", "work", "placement", "service", "नौकरी", "जॉब", "1"
        ]

        # 🟢 3. FREELANCING (Online Work, Work From Home आदि)
        freelance_keywords = [
            "freelance", "freelancing", "freelancer", "online work", "ghar baithe", "wfh", 
            "remote", "online earning", "फ्रीलांसिंग", "ऑनलाइन", "3"
        ]

        # 1️⃣ अगर स्टूडेंट ने Business चुना
        if any(k in norm_text for k in business_keywords):
            self.student.career_goal = "Business"
            self.current_stage = "business_type"
            return (
                f"शानदार **{self.student.name} जी**! अपना खुद का Business करना बहुत ही Best फ़ैसला है। 🚀\n\n"
                f"आप अपने Business में Computer का Use मुख्य रूप से किस काम के लिए करना चाहते हैं?\n\n"
                f"• Billing, Accounting और GST Manage करने के लिए\n"
                f"• Business की Digital Marketing और Online Ads चलाने के लिए\n"
                f"• Poster, Banner और Graphics Designing के लिए\n"
                f"• Website या Software Development के लिए"
            )

        # 2️⃣ अगर स्टूडेंट ने Job चुना
        elif any(k in norm_text for k in job_keywords):
            self.student.career_goal = "Job"
            self.current_stage = "job_type"
            return (
                f"बहुत बढ़िया **{self.student.name} जी**! अच्छी Job पाने के लिए सही Practical Skills होना बहुत ज़रूरी है। 💼\n\n"
                f"आप किस Type की Job Profile में Interest रखते हैं?\n\n"
                f"• Computerised Accountant\n"
                f"• Office Specialist / Executive\n"
                f"• Graphic Designer\n"
                f"• Digital Marketer\n"
                f"• Software / Python Developer"
            )

        # 3️⃣ अगर स्टूडेंट ने Freelancing चुना
        elif any(k in norm_text for k in freelance_keywords):
            self.student.career_goal = "Freelancing"
            self.current_stage = "freelancing_skill"
            return (
                f"शानदार **{self.student.name} जी**! Freelancing से आप घर बैठे देश-विदेश के Clients के लिए काम कर सकते हैं। 🌐\n\n"
                f"आप कौन सी Skill सीखकर Freelancing करना चाहते हैं?\n\n"
                f"• Graphic Designing (Logo, Banner, Social Media Posts)\n"
                f"• Digital Marketing & Content Creation\n"
                f"• Python Programming / Web Development\n"
                f"• Accounting & Data Management"
            )

        # 4️⃣ अगर समझ न आए तो विकल्प दिखाना
        else:
            return (
                f"**{self.student.name} जी**, कृपया नीचे दिए गए 3 विकल्पों में से अपना पसंदीदा लक्ष्य चुनें:\n\n"
                f"1️⃣ **Job** (अच्छी सैलरी वाली नौकरी पाना)\n"
                f"2️⃣ **Business** (खुद का काम या व्यापार बढ़ाना)\n"
                f"3️⃣ **Freelancing** (घर बैठे ऑनलाइन प्रोजेक्ट्स करना)"
            )

    # ========================================================
    # SECTION 10 : JOB TYPE HANDLER
    # ========================================================

    def handle_job_type(self, text):
        self.student.job_type = text
        self.current_stage = "qualification"
        return (
            f"समझा! **{text}** के Field में बहुत बेहतरीन Career Options हैं।\n\n"
            f"सही Course चुनने के लिए, क्या आप अपनी वर्तमान Qualification बताएंगे?\n"
            f"(जैसे: 10th, 12th, B.Com, Graduation या अन्य)"
        )

    # ========================================================
    # SECTION 11 : BUSINESS TYPE HANDLER
    # ========================================================

    def handle_business_type(self, text):
        self.student.job_type = text
        self.current_stage = "qualification"
        return (
            f"बिल्कुल सही! आपके Business को आगे बढ़ाने में यह Knowledge बहुत काम आएगी।\n\n"
            f"आपकी Qualification क्या है?"
        )

    # ========================================================
    # SECTION 12 : FREELANCING SKILL HANDLER
    # ========================================================

    def handle_freelancing_skill(self, text):
        self.student.job_type = text
        self.current_stage = "qualification"
        return (
            f"Freelancing Market में **{text}** की बहुत अच्छी Demand है!\n\n"
            f"आपकी Qualification क्या है?"
        )

    # ========================================================
    # SECTION 13 : QUALIFICATION HANDLER
    # ========================================================

    def handle_qualification(self, text):
        self.student.qualification = text
        self.current_stage = "computer_knowledge"
        return (
            f"बहुत अच्छा! **{self.student.qualification}** के साथ यह Skills आपके Resume को बहुत Strong बनाएंगी।\n\n"
            f"क्या आपको पहले से Computer की थोड़ी-बहुत Knowledge है, या बिल्कुल Basic से सीखना चाहते हैं?\n\n"
            f"1️⃣ **Basic Knowledge है** (Word, Internet आता है)\n"
            f"2️⃣ **बिल्कुल Fresher हूँ** (शुरुआत से सीखना है)"
        )

    # ========================================================
    # SECTION 14 : COMPUTER KNOWLEDGE HANDLER
    # ========================================================

    def handle_computer_knowledge(self, text):
        self.student.computer_knowledge = text
        self.current_stage = "learning_mode"
        return (
            f"बिल्कुल Clear है **{self.student.name} जी**।\n\n"
            f"आप Classes किस Mode में लेना पसंद करेंगे?\n\n"
            f"1️⃣ **Offline** (हमारे Center पर आकर Practical करना है)\n"
            f"2️⃣ **Online** (घर बैठे सीखना है)"
        )

    # ========================================================
    # SECTION 15 : LEARNING MODE HANDLER
    # ========================================================

    def handle_learning_mode(self, text):
        self.student.learning_mode = text
        self.current_stage = "recommendation_logic"
        return self.generate_recommendation()
    # ========================================================
    # SECTION 16 : RECOMMENDATION LOGIC (UPDATED PRIORITY)
    # ========================================================

    def generate_recommendation(self):
        goal = self.student.job_type.lower()
        qual = self.student.qualification.lower()
        
        # 1. First priority: User's explicit Job Goal
        if "digital" in goal or "marketing" in goal:
            self.student.recommended_course = "DIGITAL_MKTG"
        elif "graphic" in goal or "design" in goal:
            self.student.recommended_course = "GRAPHIC"
        elif "python" in goal or "programming" in goal or "coding" in goal:
            self.student.recommended_course = "PYTHON"
        elif "account" in goal or "tally" in goal or "billing" in goal:
            self.student.recommended_course = "TALLY"
        # 2. Second priority: Qualification background
        elif "b.com" in qual:
            self.student.recommended_course = "TALLY"
        elif "10th" in qual or "12th" in qual or "diploma" in goal or "adca" in goal:
            self.student.recommended_course = "ADCA"
        else:
            self.student.recommended_course = "OFFICE_EXEC"

        return self.handle_recommendation_message()
    # ========================================================
    # SECTION 17 : RECOMMENDATION MESSAGE (UPDATED)
    # ========================================================

    def handle_recommendation_message(self):
        course_key = self.student.recommended_course
        course = COURSES_DATA.get(course_key, COURSES_DATA["ADCA"])
        
        self.current_stage = "recommendation_response"
        
        response = (
            f"**{self.student.name} जी**, आपकी Profile, Goals और Qualification को ध्यान में रखते हुए "
            f"**{INSTITUTE_NAME}** का यह सुझाव है:\n\n"
            f"🎓 **Suggested Course:** {course['name']}\n"
            f"⏱️ **Course Duration:** आपके समय के अनुसार **Flexible Classes** (Regular या Fast-Track) उपलब्ध हैं, जिससे आप अपनी पसंद के अनुसार कोर्स जल्दी भी पूरा कर सकते हैं।\n"
            f"💰 **Fees Structure:** बहुत ही Affordable फीस और आसान किश्तों (Installments) की सुविधा उपलब्ध है।\n\n"
            f"इस Course में आपको केवल थ्योरी ही नहीं, बल्कि 100% Practical Projects और Computer Lab में ट्रेनिंग दी जाएगी।\n\n"
            f"😊 **{self.student.name} जी**, केवल सुनने से बेहतर है कि आप एक बार हमारे **{INSTITUTE_NAME}** सेंटर ज़रूर पधारें! "
            f"यहाँ आकर आप खुद हमारी Computer Lab देख सकते हैं, अपने टाइम के अनुसार क्लास शेड्यूल सेट कर सकते हैं और **Ramlakhan Rathor Sir** से सीधे मार्गदर्शन ले सकते हैं।\n\n"
            f"क्या आप इस Week One-Day Free Demo Class या Center Visit के लिए आना चाहेंगे?"
        )
        return response
    # ========================================================
    # SECTION 18 : RECOMMENDATION RESPONSE HANDLER (DYNAMIC LIST)
    # ========================================================

    def handle_recommendation_response(self, text):
        norm_text = text.lower()
        
        # 1. Check if student explicitly corrected the course choice
        if any(w in norm_text for w in ["digital", "marketing", "graphic", "python", "tally", "kanha tha", "bola tha", "adca", "dca", "excel"]):
            if "digital" in norm_text or "marketing" in norm_text:
                self.student.recommended_course = "DIGITAL_MKTG"
            elif "graphic" in norm_text or "design" in norm_text:
                self.student.recommended_course = "GRAPHIC"
            elif "python" in norm_text or "coding" in norm_text:
                self.student.recommended_course = "PYTHON"
            elif "tally" in norm_text or "account" in norm_text:
                self.student.recommended_course = "TALLY"
            elif "adca" in norm_text:
                self.student.recommended_course = "ADCA"
            elif "dca" in norm_text:
                self.student.recommended_course = "DCA"
            elif "excel" in norm_text:
                self.student.recommended_course = "EXCEL_ADV"
            
            course = COURSES_DATA.get(self.student.recommended_course, COURSES_DATA["ADCA"])
            return (
                f"अरे, क्षमा कीजिएगा **{self.student.name} जी**! 🙏\n\n"
                f"आपकी पसंद के अनुसार **{course['name']}** ही आपके लिए सबसे बेस्ट रहेगा।\n\n"
                f"🎓 **Course Name:** {course['name']}\n"
                f"⏱️ **Duration:** आपकी आवश्यकता अनुसार Regular या Fast-Track Option।\n"
                f"💰 **Fees:** Easy Installment Plan उपलब्ध है।\n\n"
                f"क्या आप इसके Syllabus और Classes के बारे में जानना चाहेंगे?"
            )

        # 2. Positive Response
        if any(w in norm_text for w in ["haan", "ha", "yes", "thik", "ok", "details", "बताओ", "हाँ", "जानकारी"]):
            return self.handle_course_information()

        # 3. Negative Response / Alternate Courses List Demand
        elif any(w in norm_text for w in ["nahi", "no", "ना", "नहीं", "दूसरा", "list", "कोर्स"]):
            self.current_stage = "recommendation_logic"
            
            # COURSES_DATA से डायनामिक रूप से सभी कोर्सेस की लिस्ट बनाना
            courses_list_text = "\n".join([f"• {info['name']}" for key, info in COURSES_DATA.items()])
            
            return (
                f"कोई बात नहीं **{self.student.name} जी**! हमारे **{INSTITUTE_NAME}** में आपके लिए कई अन्य Professional & Job-Oriented Courses उपलब्ध हैं:\n\n"
                f"{courses_list_text}\n\n"
                f"आप इनमें से किस Course के बारे में जानकारी या Free Demo Class लेना चाहेंगे? कृपया Course का Name बताएं।"
            )

        # 4. Default Fallback within Recommendation Response
        else:
            return self.handle_course_information()
    # ========================================================
    # SECTION 19 : COURSE INFORMATION HANDLER
    # ========================================================

    def handle_course_information(self):
        course_key = self.student.recommended_course
        course = COURSES_DATA.get(course_key, COURSES_DATA["ADCA"])
        
        self.current_stage = "course_followup"
        
        response = (
            f"📌 **{course['name']} के Key Highlights:**\n\n"
            f"1️⃣ **Practical Training:** Live Projects पर काम।\n"
            f"2️⃣ **Certification:** Course पूरा होने पर Valid Certificate।\n"
            f"3️⃣ **Flexible Batches:** Morning, Afternoon और Evening Batches।\n"
            f"4️⃣ **Easy Installments:** Fees आप किश्तों (Installments) में भी Pay कर सकते हैं।\n\n"
            f"क्या आपके मन में Fees, Timing या Classes को लेकर कोई Doubt है?"
        )
        return response

   # ========================================================
    # SECTION 20 : COURSE FOLLOW-UP HANDLER
    # ========================================================

    def handle_course_followup(self, text):
        return self.handle_free_demo_offer()

    # ========================================================
    # SECTION 21-25 : DEMO BOOKING FLOW (UPDATED)
    # ========================================================

    def handle_free_demo_offer(self):
        self.current_stage = "demo_decision"
        return (
            f"**{self.student.name} जी**, सिर्फ सुनने से बेहतर है कि आप खुद आकर Class Experience करें! 😊\n\n"
            f"हम **{INSTITUTE_NAME}** में सभी नए Students को **1 दिन की बिल्कुल Free Demo Class** देते हैं, "
            f"ताकि आप हमारी पढ़ाई का तरीका और Lab Facility देख सकें।\n\n"
            f"क्या आप अपनी Free Demo Class Book करना चाहेंगे?"
        )

    def handle_demo_decision(self, text):
        norm_text = text.lower()
        if any(w in norm_text for w in ["haan", "ha", "yes", "ok", "book", "करना", "हाँ", "ज़रूर", "जरूर", "कर दो", "demo"]):
            return self.handle_demo_booking()
        else:
            self.current_stage = "visit_decision"
            return (
                f"कोई बात नहीं **{self.student.name} जी**! अगर आप Demo Class नहीं लेना चाहते, "
                f"तो क्या आप सिर्फ हमारे Center आकर Faculty से मिलना और Guidance लेना चाहेंगे?"
            )

    def handle_demo_booking(self):
        self.current_stage = "demo_timing"
        return (
            f"बहुत बढ़िया फ़ैसला **{self.student.name} जी**! 🎉\n\n"
            f"Demo Class के लिए कौन सा Time Slot आपके लिए Best रहेगा?\n\n"
            f"1️⃣ **Morning Batch:** 8:00 AM - 11:00 AM\n"
            f"2️⃣ **Afternoon Batch:** 12:00 PM - 3:00 PM\n"
            f"3️⃣ **Evening Batch:** 4:00 PM - 7:00 PM"
        )

    def handle_demo_timing(self, text):
        self.student.selected_time_slot = text
        self.current_stage = "demo_date_time"
        return (
            f"Ok! **{text}** का Slot आपके लिए Select किया गया है। 😊\n\n"
            f"आप Free Demo Class के लिए किस दिन आना चाहेंगे? (जैसे: कल, परसों या कोई Date बताएं)"
        )

    def handle_demo_date_time_extended(self, text):
        self.student.selected_date_time = text
        self.student.demo_booked = True
        self.current_stage = "admission_decision"
        return (
            f"🎉 **Congratulations {self.student.name} जी! आपकी Free Demo Class और Batch स्लॉट Book हो गया है।**\n\n"
            f"📌 **{self.student.name} जी, आपके Batch & Class की Details नीचे दी गई हैं:**\n\n"
            f"🎓 **Course:** {self.student.recommended_course}\n"
            f"📅 **Demo Date:** {text}\n"
            f"⏰ **Batch Timing:** {self.student.selected_time_slot}\n"
            f"🏫 **Classroom / Lab:** Lab 01 (Main Computer Lab)\n"
            f"👨‍🏫 **Faculty:** {FOUNDER_NAME} Sir & Senior Faculty\n\n"
            f"आपको Class शुरू होने के 10 मिनट पहले Center पहुँचना होगा।\n"
            f"📲 **Note:** आपके मोबाइल पर 1 घंटे पहले Reminder Message भी भेज दिया जाएगा।\n\n"
            f"क्या आप अपनी सीट तुरंत रिज़र्व करके Admission Confirm करना चाहेंगे या Demo Class के बाद फ़ैसला लेंगे?"
        )
    # ========================================================
    # SECTION 26 : INSTITUTE VISIT HANDLER
    # ========================================================

    def handle_institute_visit(self):
        self.current_stage = "visit_decision"
        response = (
            f"**{self.student.name} जी**, आप जब चाहें हमारे **{INSTITUTE_NAME}** Center आ सकते हैं। "
            f"यहाँ आकर आप हमारी Computer Lab देख सकते हैं और सीधे मुझसे या हमारी Faculty से बात भी कर सकते हैं।\n\n"
            f"क्या आप इस Week Center आने का Plan बना रहे हैं?"
        )
        return response

    # ========================================================
    # SECTION 27 : VISIT DECISION HANDLER
    # ========================================================

    def handle_visit_decision(self, text):
        norm_text = text.lower()
        if any(w in norm_text for w in ["haan", "ha", "yes", "ok", "आऊँगा", "आऊंगा", "हाँ", "आना"]):
            self.current_stage = "visit_timing"
            return (
                f"बहुत बढ़िया! Center आने के लिए कौन सा Time आपके लिए सही रहेगा?\n\n"
                f"1️⃣ **Morning:** 10:00 AM से 1:00 PM के बीच\n"
                f"2️⃣ **Afternoon:** 2:00 PM से 5:00 PM के बीच"
            )
        else:
            self.current_stage = "admission_discussion"
            return self.handle_admission_discussion()

    # ========================================================
    # SECTION 28 : VISIT TIMING HANDLER
    # ========================================================

    def handle_visit_timing(self, text):
        self.student.selected_time_slot = text
        self.current_stage = "visit_date_time"
        return f"ओके! आप किस दिन (Date) Center आना चाहेंगे?"

    # ========================================================
    # SECTION 29 : VISIT DATE/TIME HANDLER
    # ========================================================

    def handle_visit_date_time(self, text):
        self.student.selected_date = text
        self.visit_scheduled = True
        return self.handle_visit_confirmation()

    # ========================================================
    # SECTION 30 : VISIT CONFIRMATION HANDLER
    # ========================================================

    def handle_visit_confirmation(self):
        self.current_stage = "admission_discussion"
        response = (
            f"🎉 **{self.student.name} जी, आपके आने का Time तय हो गया है!**\n\n"
            f"📍 **Venue:** {INSTITUTE_NAME} Campus\n"
            f"📅 **Date:** {self.student.selected_date}\n"
            f"⏰ **Time:** {self.student.selected_time_slot}\n\n"
            f"जब आप Center आएँगे, तो मैं और हमारी Team आपसे मिलेंगे और आपको पूरा Center दिखाएंगे।"
        )
        return response

   # ========================================================
    # SECTION 31 : ADMISSION DECISION HANDLER (SINGLE & FIXED)
    # ========================================================

    # Google Maps Link Handler
    def handle_google_maps_location(self):
        return (
            f"**{self.student.name if self.student.name else 'जी'}**, यह लीजिए हमारे सेंटर का Google Maps Link: 📍 https://maps.google.com/?q=SCO-17+Karnal\n\n"
            f"आप इस पर क्लिक करके आसानी से नेविगेट कर सकते हैं। सेंटर पर आपसे मुलाकात होगी! 😊"
        )

    # Admission Decision Handler (Missing Function Fix)
    def handle_admission_decision(self, text):
        norm_text = text.lower()
        if any(w in norm_text for w in ["haan", "ha", "yes", "confirm", "admission", "आज ही", "कर दो", "हाँ", "कन्फर्म", "करदो"]):
            return self.handle_admission_information()
        else:
            self.conversation_completed = True
            return (
                f"बिल्कुल **{self.student.name if self.student.name else 'जी'}**! आप आराम से Demo Class लीजिए और फिर फ़ैसला कीजिए। 😊\n\n"
                f"हम आपका **{INSTITUTE_NAME}** सेंटर पर इंतज़ार करेंगे। धन्यवाद!"
            )

    # Admission Information Handler
    def handle_admission_information(self):
        self.current_stage = "completed"
        self.conversation_completed = True
        
        # एडमिशन सेंटर विजिट के बाद ही रहेगा
        self.student.admission_status = "Pending (Demo Booked)"
        
        course_key = getattr(self.student, 'recommended_course', 'Digital Marketing')
        course_obj = COURSES_DATA.get(course_key, {}) if 'COURSES_DATA' in globals() else {}
        course_display_name = course_obj.get('name', course_key if course_key != 'DIGITAL_MKTG' else 'Digital Marketing')

        return (
            f"बहुत बढ़िया **{self.student.name if self.student.name else 'जी'}**! आपकी रुचि देखकर बहुत खुशी हुई। 🎉\n\n"
            f"हमारी पॉलिसी के अनुसार एडमिशन की प्रक्रिया सेंटर पर पधारकर, Demo Class लेने और Documents जमा करने के बाद ही पूरी होती है।\n\n"
            f"📌 मैंने आपकी **Free Demo Class और Seat Slot Reserve** कर दी है:\n"
            f"🎓 **Course:** {course_display_name}\n"
            f"🏫 **Center Address:** SCO-17, 2nd Floor, Behind Old Bus Stand, Karnal - 132001\n"
            f"📍 **Google Maps:** https://maps.google.com/?q=SCO-17+Karnal\n"
            f"📞 **Contact Numbers:** +91-7876941339, 95885-44158\n\n"
            f"आप तय समय पर सेंटर पधारें, अपनी Free Demo Class लें और उसके बाद आसानी से अपना Admission फ़ॉर्म जमा करवा सकते हैं।\n\n"
            f"**{INSTITUTE_NAME}** में आपका इंतज़ार रहेगा। धन्यवाद! 🙏"
        )

    # ========================================================
    # SECTION 33 : ADMISSION INFORMATION HANDLER (CRASH FREE)
    # ========================================================

    def handle_admission_information(self):
        self.current_stage = "completed"
        self.conversation_completed = True
        
        # 🔥 यहाँ Status को Confirmed करें (ताकि Summary में Pending न आए)
        self.student.admission_status = "Confirmed"
        
        # कोर्स का नाम प्रॉपर डिस्प्ले करने के लिए
        course_key = getattr(self.student, 'recommended_course', 'Digital Marketing')
        course_obj = COURSES_DATA.get(course_key, {}) if 'COURSES_DATA' in globals() else {}
        course_display_name = course_obj.get('name', course_key if course_key != 'DIGITAL_MKTG' else 'Digital Marketing')

        response = (
            f"🎉 **Congratulations {self.student.name if self.student.name else 'जी'}! {INSTITUTE_NAME} Family में आपका स्वागत है!**\n\n"
            f"📋 **Required Documents for Admission:**\n"
            f"1️⃣ Aadhaar Card की फोटोकॉपी\n"
            f"2️⃣ Last Marksheet की फोटोकॉपी\n"
            f"3️⃣ 2 Passport Size Photographs\n\n"
            f"📍 **Course:** {course_display_name}\n"
            f"🏫 **Center Address:** SCO-17, 2nd Floor, Behind Old Bus Stand, Karnal - 132001\n"
            f"📞 **Contact Numbers:** +91-7876941339, 95885-44158\n\n"
            f"हमारी Team जल्द ही आपसे Contact करके आपकी Seat Confirm कर देगी। Thank you!"
        )
        return response

    # ========================================================
    # SECTION 34 : UNIVERSAL QUESTION CHECKER (UPDATED & SAFE)
    # ========================================================

    def check_universal_questions(self, text):
        # 1. शुरुआती स्टेप्स (welcome, name, career_goal) में यूनिवर्सल चेक बंद रखें
        if self.current_stage in ["welcome", "name", "career_goal"]:
            return None

        norm_text = text.lower()

        # 2. अगर स्टूडेंट 'fees jyada hai' या 'kam karo' बोले, तो यह Objection है, Fees Question नहीं!
        if any(w in norm_text for w in ["jyada", "kam karo", "kam ho", "mahanga", "mahangi"]):
            return None

        # 3. बाकी सभी Universal Questions के Checks
        if any(w in norm_text for w in ["fee", "fees", "paisa", "kitne ka", "फीस", "कितने का"]):
            return self.handle_fees_question()
        elif any(w in norm_text for w in ["timing", "time", "time kya hai", "kitne hour", "kitne ghante", "ghante", "समय", "टाइम"]):
            return self.handle_timing_question()
        elif any(w in norm_text for w in ["address", "location", "kahan hai", "kaha hai", "kahan par", "पता", "कहाँ"]):
            return self.handle_address_question()
        elif any(w in norm_text for w in ["certificate", "iso", "government", "सर्टिफिकेट"]):
            return self.handle_certificate_question()
        elif any(w in norm_text for w in ["job", "placement", "salary", "नौकरी"]):
            return self.handle_placement_question()
        elif any(w in norm_text for w in ["discount", "offer", "scholarship", "छूट"]):
            return self.handle_discount_question()
        elif any(w in norm_text for w in ["demo", "demo class", "डेमो"]) and not any(w in norm_text for w in ["book", "haan", "ha", "kar do", "कर दो", "करना"]):
            return self.handle_demo_question()
        elif any(w in norm_text for w in ["map", "maps", "location link", "bhej do", "google map", "मैप"]):
            return self.handle_google_maps_location()
        elif any(w in norm_text for w in ["teacher", "faculty", "ramlakhan", "शिक्षक"]):
            return self.handle_faculty_question()

        return None

    # ========================================================
    # SECTION 35 : FEES QUESTION HANDLER (UPDATED)
    # ========================================================

    def handle_fees_question(self):
        rec_course = getattr(self.student, 'recommended_course', 'Digital Marketing')
        
        return (
            f"**{self.student.name if self.student.name else 'जी'}**, हमारे **{rec_course}** की फीस बहुत ही कम और हर Student के बजट में रखी गई है। "
            f"साथ ही आपके लिए **Easy Monthly Installments** (आसान किश्तों) और Scholarship की भी बहुत अच्छी व्यवस्था है। 😊\n\n"
            f"समय-समय पर नए Batches के लिए विशेष Offers और Discounts भी रहते हैं, जिसकी सटीक जानकारी आपको सेंटर पर मिल जाएगी।\n\n"
            f"मैं आपसे विनम्र आग्रह करूँगा कि आप एक बार **{INSTITUTE_NAME}** सेंटर ज़रूर पधारें। "
            f"यहाँ आपकी **One-Day Free Demo Class** भी रहेगी, जहाँ आप Class का माहौल, Lab और Expert Faculty देख सकते हैं और अपनी फीस का बेस्ट Best Discount Plan भी जान सकते हैं।\n\n"
            f"क्या मैं आपके लिए कल या परसों में से किसी दिन का Free Demo Slot बुक कर दूँ?"
        )

    # ========================================================
    # SECTION 36 : TIMING & DURATION QUESTION HANDLER (UPDATED)
    # ========================================================

    def handle_timing_question(self):
        return (
            f"**{self.student.name if self.student.name else 'जी'}**, हमारी Classes Students की ज़रूरत के अनुसार बहुत ही flexible होती हैं। 😊\n\n"
            f"• **Regular Classes:** Daily 1 से 1.5 घंटे की पढ़ाई व Practical Lab।\n"
            f"• **Fast-Track Classes:** यदि आपको कोर्स जल्दी पूरा करना है, तो आप रोजाना extra time (2-3 घंटे) देकर सिलेबस जल्दी कवर कर सकते हैं।\n\n"
            f"**{INSTITUTE_NAME}** में ये Batches उपलब्ध हैं:\n"
            f"• **Morning Batch:** 8:00 AM से 11:00 AM के बीच\n"
            f"• **Afternoon Batch:** 12:00 PM से 3:00 PM के बीच\n"
            f"• **Evening Batch:** 4:00 PM से 7:00 PM के बीच\n\n"
            f"आपकी ज़रूरत के हिसाब से कौन सा Time Slot सबसे सही रहेगा?"
        )

    # ========================================================
    # SECTION 37 & 38 : ADDRESS & CERTIFICATE HANDLERS (FIXED)
    # ========================================================

    def handle_address_question(self):
        if getattr(self.student, 'demo_booked', False):
            self.current_stage = "admission_decision"
        else:
            self.current_stage = "address_asked"

        return (
            f"**{self.student.name if self.student.name else 'जी'}**, **{INSTITUTE_NAME}** का Center Address नीचे दिया गया है:\n\n"
            f"📍 **Center Address:** SCO-17, 2nd Floor, Behind Old Bus Stand, Mahila Aashram Complex, Behind S.D.Model Sr. Sec. School, Karnal - 132001\n\n"
            f"📞 **Contact Numbers:** +91-7876941339, 95885-44158\n\n"
            f"क्या मैं आपको Google Maps Location Link भेज दूँ, जिससे आप आसानी से सेंटर तक पहुँच जाएँ और आपको किसी प्रकार की परेशानी न हो?"
        )
    def handle_certificate_question(self):
        return (
            f"**{self.student.name if self.student.name else 'जी'}**, **{INSTITUTE_NAME}** से Course पूरा करने पर आपको ISO Certified और Government Recognized Certificate प्रदान किया जाता है, जो सभी Private Jobs और Government Jobs के लिए 100% Valid है। 😊"
        )
    # ========================================================
    # SECTION 39 : JOB / PLACEMENT HANDLER
    # ========================================================

    def handle_placement_question(self):
        return (
            f"हमारे सभी Professional Courses में 100% Practical Training दी जाती है।\n\n"
            f"Course पूरा होने के बाद हम आपको **Resume Building**, **Interview Preparation** और **Job Assistance** में पूरी हेल्प करते हैं।"
        )

    # ========================================================
    # SECTION 40 : DISCOUNT / SCHOLARSHIP HANDLER (UPDATED)
    # ========================================================

    def handle_discount_question(self):
        return (
            f"**{self.student.name} जी**, हम मेहनती और आगे बढ़ने वाले Students की पूरी मदद करते हैं! 😊\n\n"
            f"यदि आप इस Week हमारे सेंटर पर Visit करते हैं, तो **Ramlakhan Rathor Sir** खुद आपसे मिलेंगे और आपके लिए "
            f"**Special Early-Bird Discount & Installment Support** ज़रूर फाइनल कर देंगे।\n\n"
            f"क्या आप इस हफ्ते किस दिन हमारे सेंटर आकर अपनी Free Demo Class और Discount Offer की पूरी जानकारी लेना चाहेंगे?"
        )

    # ========================================================
    # SECTION 41 : DEMO CLASS QUESTION HANDLER
    # ========================================================

    def handle_demo_question(self):
        return (
            f"जी हाँ! हम सभी Student को **1 Day की बिल्कुल Free Demo Class** देते हैं।\n\n"
            f"डेमो क्लास में आकर आप हमारे पढ़ाने का तरीका और Computer Lab देख सकते हैं।"
        )

    # ========================================================
    # SECTION 42 : FACULTY QUESTION HANDLER
    # ========================================================

    def handle_faculty_question(self):
        return (
            f"हमारे Center पर **Ramlakhan Rathor Sir** (Founder) और अनुभवी Teachers द्वारा Classes ली जाती हैं।\n\n"
            f"यहाँ आपको हर एक Topic का 100% Practical ज्ञान दिया जाता है।"
        )

    # ========================================================
    # SECTION 43–48 : OTHER SPECIFIC HANDLERS
    # ========================================================

    def handle_general_query(self, text):
        universal_reply = self.check_universal_questions(text)
        if universal_reply:
            return universal_reply
        return "जी, आपकी बात समझ आ गई। क्या आप इसके बारे में थोड़ा और विस्तार से बताएंगे?"
    # ========================================================
    # SECTION 49 : OBJECTION DETECTION SYSTEM (UPDATED)
    # ========================================================

    def check_objection(self, text):
        norm_text = text.lower()

        # 1. High Fees Objection
        if any(w in norm_text for w in ["महंगी", "mahangi", "jyada", "kam karo", "paisa nahi", "kam hai", "kam kar"]):
            return self.handle_high_fees_objection()

        # 2. Time/Schedule Objection
        if any(w in norm_text for w in ["time nahi", "samay nahi", "busy", "job karta hu", "college hai"]):
            return self.handle_no_time_objection()

        # 3. Parents / Family Approval Objection
        if any(w in norm_text for w in ["papa", "mummy", "ghar wale", "parents", "pooch kar"]):
            return self.handle_parent_approval_objection()

        # 4. Distance / Location Objection
        if any(w in norm_text for w in ["door hai", "distance", "aane me dikkat", "bahut door"]):
            return self.handle_distance_objection()

        # 5. Job Guarantee Objection
        if any(w in norm_text for w in ["job milegi", "guarantee", "job pakki", "placement"]):
            return self.handle_job_guarantee_objection()

        return None

    # ========================================================
    # SECTION 50–53 : OBJECTION SYSTEM MANAGEMENT
    # ========================================================

    def process_objection_flow(self, text):
        objection_response = self.check_objection(text)
        if objection_response:
            return objection_response
        return None

    # ========================================================
    # SECTION 54 : HIGH FEES OBJECTION HANDLER (SET STAGE FIX)
    # ========================================================

    def handle_high_fees_objection(self):
        # फ़ीस का Objection हैंडल करने के बाद अगली Stage को Demo Decision पर Set किया गया है:
        self.current_stage = "demo_decision"
        return (
            f"**{self.student.name} जी**, मैं आपकी बात बिल्कुल समझ सकता हूँ। 😊\n\n"
            f"लेकिन **{INSTITUTE_NAME}** का मकसद हर Student को Quality Education देना है। हमारी Fees दूसरी जगह की तुलना में बहुत ही Reasonable रखी गई है, क्योंकि इसमें आपको Full Practical Projects, Computer Lab support और Valid Certification मिलता है।\n\n"
            f"साथ ही, आपको एक बार में पूरी Fees नहीं देनी है — आप इसे **Easy Monthly Installments** (किश्तों) में दे सकते हैं।\n\n"
            f"क्या आप अपनी **One-Day Free Demo Class** बुक करके एक बार Center Visit करना चाहेंगे?"
        )

    # ========================================================
    # SECTION 55 : NO TIME / BUSY SCHEDULE OBJECTION HANDLER
    # ========================================================

    def handle_no_time_objection(self):
        return (
            f"**{self.student.name} जी**, Time की दिक्कत समझना बिल्कुल जायज है! "
            f"इसीलिए हमारे Center पर College स्टूडेंट्स और Working Professionals के लिए **Flexible Timing Batches** उपलब्ध हैं।\n\n"
            f"हमारे पास Early Morning (8 AM) और Late Evening (6 PM) के विशेष Batches भी हैं। "
            f"आप दिन में केवल 1 घंटे का Time निकालकर आसानी से Skill सीख सकते हैं।\n\n"
            f"क्या आपके लिए Morning या Evening में से कोई स्लॉट सुविधाजनक रहेगा?"
        )

    # ========================================================
    # SECTION 56 : PARENTS / FAMILY APPROVAL OBJECTION HANDLER
    # ========================================================

    def handle_parent_approval_objection(self):
        return (
            f"बिल्कुल सही बात है **{self.student.name} जी**! Career का कोई भी बड़ा Step लेने से पहले Parents की सलाह लेना बहुत ज़रूरी होता है।\n\n"
            f"आप चाहें तो अपने Parents को भी हमारे Center साथ ला सकते हैं। "
            f"हम और **Ramlakhan Rathor Sir** खुद उनसे मिलेंगे, उन्हें पूरे Course, Career Scope और Job Placement के बारे में समझाएंगे।\n\n"
            f"क्या आप इस Weekend अपने Parents के साथ Center आने का Plan बनाना चाहेंगे?"
        )

    # ========================================================
    # SECTION 57 : DISTANCE / LOCATION OBJECTION HANDLER
    # ========================================================

    def handle_distance_objection(self):
        return (
            f"अगर Center थोड़ा दूर है, तो आप चिंता मत कीजिए **{self.student.name} जी**! "
            f"हमारे पास **Live Interactive Online Classes** का भी Option उपलब्ध है।\n\n"
            f"आप घर बैठे अपने Mobile या Laptop से पूरी Practical Training ले सकते हैं और आपको Same Center Certification मिलेगा।\n\n"
            f"क्या आप 1 दिन की Free Online Demo Class लेकर देखना चाहेंगे?"
        )

    # ========================================================
    # SECTION 58 : JOB GUARANTEE OBJECTION HANDLER
    # ========================================================

    def handle_job_guarantee_objection(self):
        return (
            f"**{self.student.name} जी**, **{INSTITUTE_NAME}** में हमारा पूरा Focus Practical Knowledge देने पर रहता है। "
            f"जब आपके पास Real Skills होंगी, तो Jobs खुद आपके पास आएंगी।\n\n"
            f"Course पूरा होने के बाद हम हर Student को **100% Placement Assistance**, Resume Building और Mock Interview Preparation में पूरी मदद करते हैं।\n\n"
            f"क्या आप हमारे यहाँ से Pass-out हुए Students के Placement Success Stories देखना चाहेंगे?"
        )

    # ========================================================
    # SECTION 59 : ONLINE MODE DOUBT HANDLER
    # ========================================================

    def handle_online_doubt_objection(self):
        return (
            f"कई Students को लगता है कि Online पढ़ाई समझ आएगी या नहीं, यह सोचना स्वाभाविक है **{self.student.name} जी**।\n\n"
            f"लेकिन हमारी Online Classes रिकॉर्डेड नहीं, बल्कि **Live & Interactive** होती हैं, जहाँ आप Teacher से तुरंत सवाल पूछ सकते हैं। "
            f"साथ ही, Screen Sharing के ज़रिये Practical Work कराया जाता है।\n\n"
            f"इसे खुद Check करने के लिए आप 1 Day Free Demo Class लेकर देख सकते हैं। क्या मैं आपकी Free Demo Book कर दूँ?"
        )

    # ========================================================
    # SECTION 60 : THINKING / DELAY OBJECTION HANDLER
    # ========================================================

    def handle_thinking_objection(self):
        return (
            f"ज़रूर **{self.student.name} जी**, सोच-समझकर फैसला लेना बहुत अच्छी बात है! 👍\n\n"
            f"बस ध्यान रखें कि हमारे नए Practical Batches में Seats लिमिटेड होती हैं। "
            f"यदि आप 1 Day Free Demo Class ले लें, तो आपको Decision लेने में और भी आसानी होगी।\n\n"
            f"क्या हम कल के लिए आपकी Free Demo Seat Hold कर दें?"
        )

    # ========================================================
    # SECTION 61–67 : ADDITIONAL SPECIFIC OBJECTION HANDLERS
    # ========================================================

    def handle_general_objection(self, text):
        objection_reply = self.check_objection(text)
        if objection_reply:
            return objection_reply
        return f"**{self.student.name} जी**, आपकी बात बिल्कुल सही है। अगर आपके मन में कोई और Doubt है तो बेझिझक बताइए, मैं आपकी पूरी Help करूँगा।"
    # ========================================================
    # SECTION 68 : COMPLETED CONVERSATION HANDLER
    # ========================================================

    def handle_completed_stage(self, text):
        """
        जब Student का Admission या Demo/Visit Booking पूरा हो चुका हो
        """
        sentiment = self.detect_sentiment(text)
        
        if sentiment == "positive":
            return (
                f"बहुत-बहुत धन्यवाद **{self.student.name} जी**! 😊\n\n"
                f"आपकी डिटेल्स हमारे पास सेव हो चुकी हैं। अगर आपको रास्ते या Timing से जुड़ा "
                f"कोई भी सवाल पूछना हो, तो आप बेझिझक यहाँ मैसेज कर सकते हैं।"
            )
        else:
            return (
                f"**{self.student.name} जी**, आपका Admission / Booking Process पहले ही दर्ज हो चुका है।\n\n"
                f"हमारी Team जल्द ही आपसे Direct Contact करेगी। किसी भी Urgent Help के लिए आप हमारे Contact Number पर कॉल कर सकते हैं।"
            )

    # ========================================================
    # SECTION 69 : FOLLOW-UP SYSTEM
    # ========================================================

    def handle_followup_system(self, text):
        """
        Student के पुराने Response के आधार पर Follow-up मैसेज जेनरेट करना
        """
        if self.demo_booked:
            return (
                f"**{self.student.name} जी**, आपकी Free Demo Class scheduled है।\n"
                f"Date: **{self.student.selected_date}** | Time: **{self.student.selected_time_slot}**\n\n"
                f"क्या आप टाइम पर Center पहुँच रहे हैं?"
            )
        elif self.visit_scheduled:
            return (
                f"**{self.student.name} जी**, आपकी Campus Visit scheduled है।\n"
                f"Date: **{self.student.selected_date}** | Time: **{self.student.selected_time_slot}**\n\n"
                f"क्या आपको Center का Location ढूंढने में कोई समस्या तो नहीं हो रही?"
            )
        else:
            return (
                f"**{self.student.name} जी**, आपके Career Goal (**{self.student.job_type}**) के लिए "
                f"**{COURSES_DATA.get(self.student.recommended_course, COURSES_DATA['ADCA'])['name']}** सबसे Best Option है।\n\n"
                f"क्या हम आपकी 1 Day Free Demo Class Book कर दें?"
            )

    # ========================================================
    # SECTION 70 : SENTIMENT DETECTION ENGINE (POSITIVE / NEGATIVE / AMBIGUOUS)
    # ========================================================

    def detect_sentiment(self, text):
        """
        Student के मैसेज में से Positive, Negative और Ambiguous इंटेंट की पहचान करना
        """
        norm_text = text.lower()

        # Positive Keywords (सहमति, उत्साह, रेडी होना)
        positive_keywords = [
            "haan", "ha", "yes", "yep", "ok", "okay", "sure", "thik hai", "thik",
            "sahi hai", "agree", "interested", "book kar do", "kar do", "aunga",
            "aungi", "aaunga", "admission lena hai", "demo chahiye", "join karna hai",
            "हाँ", "हा", "सही है", "ठीक है", "आऊंगा", "आऊंगी", "एडमिशन लेना है"
        ]

        # Negative / Rejection Keywords (मना करना, संदेह, शिकायत, अन्य संस्थान)
        negative_keywords = [
            "nahi", "na", "no", "nope", "not interested", "bekar", "bakwas",
            "paisa nahi hai", "time nahi hai", "door hai", "kahi aur join kar liya",
            "fraud", "fake", "papa ne mana kiya", "mummy ne mana kiya", "exam hai",
            "nahi aunga", "nahi aungi", "cancel kar do", "mat karo",
            "नहीं", "ना", "इंटरेस्ट नहीं है", "पैसा नहीं है", "टाइम नहीं है", "मना कर दिया"
        ]

        # Ambiguous / Confused Keywords (सोचना, अनिश्चितता, उलझन)
        ambiguous_keywords = [
            "soch kar batunga", "sochungi", "dekhte hai", "maybe", "not sure",
            "confused", "baad me", "kal batunga", "pata nahi", "pooch ke batunga",
            "सोचकर बताऊंगा", "देखते हैं", "बाद में", "पता नहीं", "कन्फ्यूज हूँ"
        ]

        if any(w in norm_text for w in negative_keywords):
            return "negative"
        elif any(w in norm_text for w in positive_keywords):
            return "positive"
        elif any(w in norm_text for w in ambiguous_keywords):
            return "ambiguous"
        
        return "neutral"

    # ========================================================
    # SECTION 71 : POSITIVE RESPONSE HANDLER
    # ========================================================

    def handle_positive_response(self, text):
        """
        Student के Positive Reaction आने पर अगला Step लेना
        """
        if self.current_stage == "recommendation_response":
            return self.handle_course_information()
        elif self.current_stage == "demo_decision":
            return self.handle_demo_booking()
        elif self.current_stage == "visit_decision":
            self.current_stage = "visit_timing"
            return (
                f"बहुत बढ़िया **{self.student.name} जी**! 🎉\n\n"
                f"Center Visit के लिए कौन सा Time आपके लिए बेस्ट रहेगा?\n"
                f"1️⃣ Morning: 10:00 AM - 1:00 PM\n"
                f"2️⃣ Afternoon: 2:00 PM - 5:00 PM"
            )
        elif self.current_stage == "admission_decision":
            self.admission_confirmed = True
            return self.handle_admission_information()
        else:
            return f"बहुत अच्छा **{self.student.name} जी**! आगे की प्रक्रिया शुरू करते हैं।"

    # ========================================================
    # SECTION 72 : DETAILED NEGATIVE / REJECTION HANDLER
    # ========================================================

    def handle_negative_response(self, text):
        """
        Student द्वारा दिए गए हर तरह के Rejection का Respectful और Logical उत्तर देना
        """
        norm_text = text.lower()

        # Case 1: Joined Elsewhere (कहीं और एडमिशन ले लिया)
        if any(w in norm_text for w in ["kahi aur", "dusre institute", "join kar liya", "dusri jagah"]):
            return (
                f"कोई बात नहीं **{self.student.name} जी**! आपके Bright Future के लिए हमारी तरफ से बहुत-बहुत शुभकामनाएँ। 👍\n\n"
                f"अगर भविष्य में कभी आपको Advanced Practical Training, Projects या Software Certifications की ज़रूरत पड़े, "
                f"तो **{INSTITUTE_NAME}** के दरवाज़े आपके लिए हमेशा खुले हैं।"
            )

        # Case 2: Financial / Money Issues (पैसों की तंगी)
        elif any(w in norm_text for w in ["paisa nahi", "paise ki dikkat", "budget nahi"]):
            return (
                f"**{self.student.name} जी**, हम समझ सकते हैं कि कभी-कभी Financial Situations कठिन होती हैं।\n\n"
                f"इसीलिए हमारी संस्था में **Scholarship Options** और बहुत ही छोटी **Easy Installments** की सुविधा है। "
                f"आप केवल ₹500 - ₹1000 से भी अपनी पढ़ाई शुरू कर सकते हैं।\n\n"
                f"क्या आप हमारे Scholarship Coordinator से बात करना चाहेंगे?"
            )

        # Case 3: Distance / Transportation Issue (बहुत दूर है)
        elif any(w in norm_text for w in ["door hai", "distance", "aane me dikkat", "transport"]):
            return (
                f"**{self.student.name} जी**, Distance की वजह से अपनी Skills से Compromise मत कीजिए।\n\n"
                f"आप घर बैठे हमारी **Live Interactive Online Classes** जॉइन कर सकते हैं, जहाँ आपको Same Level की Practical Knowledge और Certificate मिलेगा।"
            )

        # Case 4: Exam / College Pressure (एग्जाम चल रहे हैं)
        elif any(w in norm_text for w in ["exam hai", "paper chal rahe", "college exam"]):
            return (
                f"बिल्कुल **{self.student.name} जी**, पहले आप अपने Exams पर पूरा Focus कीजिए! 👍\n\n"
                f"आप Exams खत्म होने के बाद नए Fresh Batch से Join कर सकते हैं। तब तक के लिए हम आपकी Seat Hold पर रख सकते हैं।"
            )

        # Case 5: Family / Parents Denied (घर वालों ने मना कर दिया)
        elif any(w in norm_text for w in ["papa ne mana", "mummy ne mana", "ghar wale nahi"]):
            return (
                f"कोई बात नहीं **{self.student.name} जी**। Parents हमेशा अपने बच्चों की भलाई सोचते हैं।\n\n"
                f"अगर आप चाहें तो हम Direct आपके Parents से बात करके उन्हें इस Course के Career Scope और Job Placement के बारे में समझा सकते हैं।"
            )

        # Case 6: Generic Rejection (साधारण मना करना)
        else:
            return (
                f"कोई बात नहीं **{self.student.name} जी**, मैं आपकी बात समझता हूँ। 😊\n\n"
                f"जब भी आप Future में अपने Career या Computer Skills को लेकर आगे बढ़ना चाहें, "
                f"आप **{INSTITUTE_NAME}** से संपर्क कर सकते हैं। आपका दिन शुभ हो!"
            )

    # ========================================================
    # SECTION 73 : AMBIGUOUS / CONFUSED RESPONSE HANDLER
    # ========================================================

    def handle_ambiguous_response(self, text):
        """
        जब Student उलझन में हो या साफ़ जवाब न दे रहा हो
        """
        return (
            f"**{self.student.name} जी**, ऐसा लगता है कि आप अभी सही Decision लेने में थोड़े Unsure हैं।\n\n"
            f"कोई बात नहीं! किसी भी समस्या का सबसे आसान हल यह है कि आप **1 Day Free Demo Class** लेकर खुद Experience करें। "
            f"इसमें आपको कोई Fees नहीं देनी है।\n\n"
            f"क्या हम कल के लिए आपकी Free Demo Class का स्लॉट बुक कर दें?"
        )

    # ========================================================
    # SECTION 74 : SENTIMENT ROUTING CONTROLLER
    # ========================================================

    def process_sentiment_routing(self, text):
        sentiment = self.detect_sentiment(text)
        
        if sentiment == "positive":
            return self.handle_positive_response(text)
        elif sentiment == "negative":
            return self.handle_negative_response(text)
        elif sentiment == "ambiguous":
            return self.handle_ambiguous_response(text)
        
        return None

    # ========================================================
    # SECTION 75 : HELPER - TEXT CLEANING & NORMALIZATION
    # ========================================================

    def clean_text(self, text):
        """
        Text में से फालतू Spaces और Characters हटाना
        """
        if not text:
            return ""
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    # ========================================================
    # SECTION 76 : HELPER - NAME EXTRACTION
    # ========================================================

    def extract_name(self, text):
        """
        Student के इनपुट में से Name निकालना
        """
        cleaned = self.clean_text(text)
        # Remove common greetings or prefixes
        cleaned = re.sub(r'(?i)(mera naam|my name is|i am|naam|namaste|hello|hi)\s*', '', cleaned)
        words = cleaned.split()
        if words:
            # First 2 words max for name
            name = " ".join(words[:2]).title()
            return name
        return ""

    # ========================================================
    # SECTION 77 : HELPER - YOUTUBE COMMENT MODERATION & AUTO-REPLY
    # ========================================================

    def check_youtube_comment_moderation(self, comment_text):
        """
        YouTube Comments को चेक करना - Delete योग्य या Reply योग्य
        """
        norm_comment = comment_text.lower()

        # 1. Check for Forbidden / Abusive / Spam Keywords
        for word in self.forbidden_keywords:
            if word in norm_comment:
                return {
                    "action": "DELETE",
                    "reason": f"Forbidden keyword detected: {word}",
                    "reply": None
                }

        # 2. Check for Course / Fees Queries on YouTube
        if any(w in norm_comment for w in ["fees", "fee", "kitne ka hai", "course", "address", "location"]):
            reply_msg = (
                f"नमस्ते! **{INSTITUTE_NAME}** में आपका स्वागत है। 🙏\n\n"
                f"हमारे सभी Courses (ADCA, Tally Prime, Graphic Designing, Python) की पूरी Details और "
                f"Free Demo Class Book करने के लिए हमसे WhatsApp/Call पर संपर्क करें: 9876543210"
            )
            return {
                "action": "REPLY",
                "reason": "Course / Fees inquiry detected",
                "reply": reply_msg
            }

        # 3. Check for Appreciation / Praise Comments
        elif any(w in norm_comment for w in ["nice", "good", "great", "best teacher", "sir badhiya", "thank you", "thanks"]):
            reply_msg = f"बहुत-बहुत धन्यवाद! **{INSTITUTE_NAME}** के साथ जुड़े रहें और अपनी Skills बढ़ाते रहें। 😊👍"
            return {
                "action": "REPLY",
                "reason": "Appreciation comment",
                "reply": reply_msg
            }

        # 4. Default Action for General Comments
        return {
            "action": "ALLOW",
            "reason": "Standard comment",
            "reply": None
        }

    # ========================================================
    # SECTION 78 : HELPER - PHONE NUMBER EXTRACTION
    # ========================================================

    def extract_phone_number(self, text):
        """
        Text से 10 अंकों का Mobile Number निकालना
        """
        match = re.search(r'\b[6-9]\d{9}\b', text)
        if match:
            return match.group(0)
        return None

    # ========================================================
    # SECTION 79 : HELPER - DATE & TIME EXTRACTION
    # ========================================================

    def extract_date_time(self, text):
        """
        Text से Date या Time पहचानना
        """
        norm_text = text.lower()
        if "kal" in norm_text or "tomorrow" in norm_text:
            return "Tomorrow"
        elif "parso" in norm_text:
            return "Day after tomorrow"
        elif "today" in norm_text or "aaj" in norm_text:
            return "Today"
        return text

    # ========================================================
    # SECTION 80 : HELPER - STUDENT PROFILE SUMMARY FORMATTER
    # ========================================================

    def format_student_summary(self):
        """
        Student की पूरी प्रोफाइल का Summary तैयार करना
        """
        course_info = COURSES_DATA.get(self.student.recommended_course, {})
        summary = (
            f"📋 **Student Profile Summary:**\n"
            f"• **Name:** {self.student.name if self.student.name else 'N/A'}\n"
            f"• **Career Goal:** {self.student.career_goal} ({self.student.job_type})\n"
            f"• **Qualification:** {self.student.qualification}\n"
            f"• **Computer Knowledge:** {self.student.computer_knowledge}\n"
            f"• **Learning Mode:** {self.student.learning_mode}\n"
            f"• **Recommended Course:** {course_info.get('name', 'N/A')}\n"
            f"• **Demo Booked:** {'Yes' if self.demo_booked else 'No'}\n"
            f"• **Visit Scheduled:** {'Yes' if self.visit_scheduled else 'No'}\n"
            f"• **Admission Status:** {'Confirmed' if self.admission_confirmed else 'Pending'}"
        )
        return summary

    # ========================================================
    # SECTION 81 : HELPER - RESET CONVERSATION
    # ========================================================

    def reset_conversation(self):
        """
        नये Student के लिए पूरा Session Reset करना
        """
        self.student = StudentProfile()
        self.current_stage = "welcome"
        self.previous_stage = ""
        self.session_active = True
        self.conversation_completed = False
        self.is_interested = False
        self.demo_booked = False
        self.visit_scheduled = False
        self.admission_confirmed = False
        self.conversation_history = []
        return "Conversation has been reset successfully."

    # ========================================================
    # SECTION 82 : HELPER - GET CURRENT STAGE
    # ========================================================

    def get_current_stage(self):
        return self.current_stage

    # ========================================================
    # SECTION 83 : HELPER - CHECK SESSION COMPLETION
    # ========================================================

    def is_session_completed(self):
        return self.conversation_completed

    # ========================================================
    # SECTION 84 : FALLBACK ENGINE & SMART Q&A
    # ========================================================

    def handle_fallback(self, text):
        """
        जब AI को Student का मैसेज समझ न आए या वह Fees/Address/Courses/Demo पूछे
        """
        if not self.student.name:
            return "क्षमा करें, मैं आपका Name ठीक से समझ नहीं पाया। कृपया अपना शुभ Name दोबारा बताएं?"

        norm_text = text.lower().strip()

        # 1️⃣ FEES & INSTALLMENTS
        if any(k in norm_text for k in ["fee", "fees", "kitna lagega", "paisa", "rupee", "installment", "2", "cost"]):
            return (
                f"**{self.student.name} जी**, हमारे यहाँ सभी Courses की Fees बहुत ही Affordable और बजट के अनुकूल है। 💳\n\n"
                f"• **Easy Installments (आसान किश्तों)** की सुविधा उपलब्ध है।\n"
                f"• Early Admission पर विशेष **Scholarship / Discount** भी दिया जाता है।\n\n"
                f"सटीक Fees व Discount Offer जानने के लिए आप हमारे Center पर Visit कर सकते हैं या Helpline पर संपर्क कर सकते हैं! 😊"
            )

        # 2️⃣ CENTER ADDRESS / LOCATION / ROUTE / KAISE AAU
        elif any(k in norm_text for k in ["address", "location", "kaha hai", "kahan", "center", "centre", "kaha par", "map", "maps", "google map", "kaise aau", "kaise pahuchu", "kaise aana hai", "rasta", "route", "4"]):
            return (
                f"**{self.student.name} जी**, Center पहुँचना बहुत ही आसान है:\n\n"
                f"📍 **Learning Point Destination**\n"
                f"🏢 Main Campus, Near Central Market / Bus Stand\n"
                f"🗺️ **Google Maps Link:** https://maps.google.com/?q=Learning+Point+Destination\n"
                f"📞 **Helpline:** 9588544158\n\n"
                f"आप ऊपर दिए गए Google Map लिंक को खोलकर सीधे नेविगेशन ऑन कर सकते हैं। Center पहुँचने पर कॉल कर लीजिएगा!"
            )
            return (
            f"बहुत बढ़िया **{self.student.name} जी**! 🎉\n\n"
            f"आपकी **1-Day Free Practical Demo Class** के लिए रिक्वेस्ट नोट कर ली गई है।\n\n"
            f"आप कल अपनी सुविधानुसार Center पर आकर Class ले सकते हैं।\n\n"
            f"🏢 **Center Address:** Learning Point Destination, Main Campus, Near Central Market / Bus Stand\n"
            f"🗺️ **Google Maps Link:** https://maps.google.com/?q=Learning+Point+Destination\n"
            f"📞 **Counselor Helpline:** 9588544158\n\n"
            f"क्या आपको Center पहुँचने का रास्ता (Route) जानने या किसी अन्य चीज़ में कोई सहायता चाहिए? 😊"
         )
         # 🟢 Abroad / Foreign / Out of India Query Handler
        elif any(k in norm_text for k in ["usa", "america", "abroad", "videsh", "foreign", "canada", "dubai", "gulf", "bahar"]):
            return (
                f"**{self.student.name} जी**, अगर आप Foreign / Abroad (जैसे USA, Canada, Gulf) में Career बनाना चाहते हैं, "
                f"तो International Level पर इन IT व Tech Skills की सबसे ज़्यादा डिमांड है:\n\n"
                f"1. 💻 **Full Stack Web / Software Development (Python / MERN)**\n"
                f"2. 📊 **Data Analytics with Power BI & Advanced Excel**\n"
                f"3. 🚀 **Advanced Digital Marketing & SEO**\n\n"
                f"हमारे Center पर इन सभी के Practical & Industry Standard कोर्सेज कराए जाते हैं।\n"
                f"क्या आप इनमें से किसी Course की Details जानना चाहते हैं?"
            )  
        # 🟢 Visa / Passport / Non-Institute Queries
        elif any(k in norm_text for k in ["visa", "passport", "embassy", "ticket", "flight"]):
            return (
                f"**{self.student.name} जी**, हम **Learning Point Destination** में केवल Professional Computer & IT Courses की प्रैक्टिकल ट्रेनिंग प्रदान करते हैं, Visa या Immigration की सुविधा हमारे यहाँ उपलब्ध नहीं है। ✈️\n\n"
                f"हाँ, विदेश में अच्छी जॉब पाने के लिए यदि आपको कोई **Technical / Computer Skill** सीखनी हो, तो हम आपकी पूरी मदद कर सकते हैं। 😊"
            )
        # 4️⃣ COURSE / SYLLABUS / POWER BI / SPECIFIC COURSES
        elif any(k in norm_text for k in ["course", "syllabus", "power bi", "excel", "python", "digital", "tally", "graphic", "1"]):
            course_name = "Power BI & Data Analytics" if "power bi" in norm_text else "इस Course"
            return (
                f"**{self.student.name} जी**, **{course_name}** में आपको:\n\n"
                f"✅ 100% Practical Training on Real Projects\n"
                f"✅ Industry Standard Tools & Live Case Studies\n"
                f"✅ ISO Certified & Govt. Recognized Certificate 📜\n"
                f"✅ Job Assistance & Resume Building Support\n\n"
                f"क्या आप इसके लिए Free Demo Class बुक करना चाहेंगे?"
            )

        # 5️⃣ DEFAULT FALLBACK (जब बिल्कुल कुछ मैच न हो)
        return (
            f"**{self.student.name} जी**, मैं आपकी बात पूरी तरह समझ नहीं पाया। 😊\n\n"
            f"क्या आप अपना सवाल दोबारा पूछ सकते हैं, या इनमें से किसी Option पर जानकारी चाहते हैं?\n"
            f"1️⃣ Course & Syllabus Details\n"
            f"2️⃣ Course Fees & Installments\n"
            f"3️⃣ Free Demo Class Booking\n"
            f"4️⃣ Center Address & Location"
        )

    # ========================================================
    # SECTION 85 : REPEATED UNCLEAR INPUT RECOVERY
    # ========================================================

    def handle_repeated_unclear_inputs(self):
        """
        बार-बार अमान्य (Unclear) इनपुट आने पर Help Representative का विकल्प देना
        """
        return (
            f"**{self.student.name} जी**, ऐसा लगता है कि आपके सवाल को समझने में मुझे थोड़ी कठिनाई हो रही है।\n\n"
            f"आप सीधे **Ramlakhan Rathor Sir** या हमारे Senior Counselor से बात कर सकते हैं:\n"
            f"📞 **Counseling Helpline:** 9876543210\n"
            f"📍 **Center Address:** Learning Point Destination Campus\n\n"
            f"हमारी Team आपकी पूरी सहायता करेगी!"
        )

    # ========================================================
    # SECTION 86 : FINAL SYSTEM STATUS REPORT
    # ========================================================

    def get_final_system_status(self):
        """
        सिस्टम का अंतिम स्टेटस और लॉग्स प्राप्त करना
        """
        return {
            "platform": PROJECT_NAME,
            "version": VERSION,
            "institute": INSTITUTE_NAME,
            "founder": FOUNDER_NAME,
            "current_stage": self.current_stage,
            "completed": self.conversation_completed,
            "student_summary": self.format_student_summary()
        }
    # ========================================================
    # SECTION 87 : BATCH MANAGEMENT CONSTANTS & LAB ALLOCATION
    # ========================================================

    # इंस्टिट्यूट के बैचेस और लैब आवंटन की जानकारी
    BATCH_SCHEDULE_DATA = {
        "MORNING": {
            "time_slot": "8:00 AM - 11:00 AM",
            "lab_room": "Lab 01 (Main Computer Lab)",
            "instructor": "Ramlakhan Rathor Sir & Senior Faculty",
            "upcoming_batch_start": "Every Monday"
        },
        "AFTERNOON": {
            "time_slot": "12:00 PM - 3:00 PM",
            "lab_room": "Lab 02 (Advanced Practical Lab)",
            "instructor": "Senior Tech Faculty",
            "upcoming_batch_start": "Every Monday"
        },
        "EVENING": {
            "time_slot": "4:00 PM - 7:00 PM",
            "lab_room": "Lab 01 (Main Computer Lab)",
            "instructor": "Ramlakhan Rathor Sir & Senior Faculty",
            "upcoming_batch_start": "Every Monday"
        }
    }

    # ========================================================
    # SECTION 88 : BATCH ALLOCATION HANDLER (OPTION C)
    # ========================================================

    def handle_batch_allocation(self):
        """
        Student के चुने गए टाइम स्लॉट के आधार पर Batch, Lab Room और Date की जानकारी देना
        """
        self.current_stage = "batch_assigned"
        slot_text = self.student.selected_time_slot.lower()

        # Batch Key तय करना
        if "morning" in slot_text or "8" in slot_text or "9" in slot_text or "10" in slot_text:
            batch_key = "MORNING"
        elif "afternoon" in slot_text or "12" in slot_text or "1" in slot_text or "2" in slot_text:
            batch_key = "AFTERNOON"
        else:
            batch_key = "EVENING"

        batch = self.BATCH_SCHEDULE_DATA[batch_key]
        course_key = self.student.recommended_course
        course_name = COURSES_DATA.get(course_key, COURSES_DATA["ADCA"])["name"]

        response = (
            f"📌 **{self.student.name} जी, आपके Batch & Class की Details नीचे दी गई हैं:**\n\n"
            f"🎓 **Course:** {course_name}\n"
            f"📅 **New Batch Start Date:** Upcoming {batch['upcoming_batch_start']}\n"
            f"⏰ **Batch Timing:** {batch['time_slot']}\n"
            f"🏫 **Classroom / Lab:** {batch['lab_room']}\n"
            f"👨‍🏫 **Faculty:** {batch['instructor']}\n\n"
            f"आपको Class शुरू होने के 10 मिनट पहले Center पहुँचना होगा।"
        )
        return response

    # ========================================================
    # SECTION 89 : AUTOMATED REMINDER SCHEDULER (OPTION B)
    # ========================================================

    def schedule_automated_reminder(self, reminder_type="DEMO"):
        """
        Demo या Visit के लिए Reminder Data Structure तैयार करना
        """
        course_key = getattr(self.student, 'recommended_course', 'ADCA')
        course_obj = COURSES_DATA.get(course_key, {}) if 'COURSES_DATA' in globals() else {}
        course_name = course_obj.get('name', 'Computer Course')

        # Fix: selected_date ki jagah getattr ya selected_date_time use karen
        date_val = getattr(self.student, 'selected_date_time', '') or getattr(self.student, 'selected_date', 'Scheduled Date')

        if reminder_type == "DEMO":
            msg = (
                f"⏰ **REMINDER - Free Demo Class**\n\n"
                f"नमस्ते **{self.student.name} जी**! 🙏\n"
                f"**{INSTITUTE_NAME}** में आपकी **{course_name}** की Free Demo Class scheduled है:\n\n"
                f"📅 **Date:** {date_val}\n"
                f"⏰ **Time:** {self.student.selected_time_slot}\n"
                f"📍 **Venue:** Learning Point Destination Campus\n\n"
                f"कृपया समय पर पधारें। किसी भी सहायता के लिए कॉल करें: 9876543210"
            )
        elif reminder_type == "VISIT":
            msg = (
                f"⏰ **REMINDER - Center Visit**\n\n"
                f"नमस्ते **{self.student.name} जी**! 🙏\n"
                f"आज आपका **{INSTITUTE_NAME}** सेंटर विजिट का प्लान तय हुआ था:\n\n"
                f"📅 **Date:** {date_val}\n"
                f"⏰ **Time:** {self.student.selected_time_slot}\n"
                f"📍 **Location:** Learning Point Destination Campus\n\n"
                f"मैं और हमारी टीम आपका इंतज़ार कर रहे हैं!"
            )
        else:
            msg = (
                f"⏰ **REMINDER - Batch Starting Soon**\n\n"
                f"नमस्ते **{self.student.name} जी**! आपकी **{course_name}** की क्लासेस जल्द शुरू हो रही हैं। "
                f"तैयारी पूरी रखें!"
            )

        reminder_payload = {
            "student_name": self.student.name,
            "reminder_type": reminder_type,
            "scheduled_date": date_val,
            "scheduled_time": self.student.selected_time_slot,
            "message_body": msg,
            "status": "SCHEDULED"
        }
        return reminder_payload

   # ========================================================
    # SECTION 90 : DEMO CONFIRMATION WITH BATCH & PHONE NUMBER
    # ========================================================

    def handle_demo_date_time_extended(self, text):
        self.student.selected_date_time = text
        self.student.demo_booked = True
        self.demo_booked = True
        self.current_stage = "ask_phone"
        
        return (
            f"बहुत बढ़िया **{self.student.name} जी**! 👍\n\n"
            f"आपकी Demo Seat की डिटेल्स और SMS Reminder भेजने के लिए, कृपया अपना **10 अंकों का Mobile Number** दर्ज करें:"
        )

    def handle_phone_submission(self, text):
        phone_num = self.extract_phone_number(text)
        if not phone_num:
            return "कृपया सही 10 अंकों का Mobile Number दर्ज करें (जैसे: 9876543210)।"

        self.student.phone = phone_num
        self.student.admission_status = "Pending (Demo Booked)"
        self.current_stage = "admission_decision"

        # 🟢 Google Sheet में Automatic Data Save
        self.save_student_to_sheet()

        batch_info = self.handle_batch_allocation()

        return (
            f"🎉 **Congratulations {self.student.name} जी! आपकी Free Demo Class और Batch स्लॉट Book हो गया है।**\n\n"
            f"{batch_info}\n\n"
            f"📱 **Registered Mobile:** {self.student.phone}\n"
            f"📲 **Note:** आपके इस मोबाइल नंबर पर 1 घंटे पहले Reminder Message भेज दिया जाएगा。\n\n"
            f"क्या आप अपनी सीट तुरंत रिज़र्व करके Admission Confirm करना चाहेंगे या Demo Class के बाद फ़ैसला लेंगे?"
        )

    # ========================================================
    # SECTION 91 : VISIT CONFIRMATION WITH REMINDER
    # ========================================================
    
    def handle_visit_date_time_extended(self, text):
        """
        Center Visit Confirm होने पर Reminder सेट करना और Google Sheet में Save करना
        """
        self.student.selected_date = text
        self.student.selected_date_time = text
        self.visit_scheduled = True
        self.student.admission_status = "Pending (Visit Scheduled)"

        # 🟢 Google Sheet में Automatic Data Save
        self.save_student_to_sheet()

        reminder_data = self.schedule_automated_reminder(reminder_type="VISIT")

        response = (
            f"🎉 **{self.student.name} जी, आपके आने का Time और Campus Visit कन्फर्म हो गया है!**\n\n"
            f"📍 **Venue:** {INSTITUTE_NAME} Campus\n"
            f"📅 **Date:** {self.student.selected_date}\n"
            f"⏰ **Time:** {self.student.selected_time_slot}\n\n"
            f"📲 **Reminder Notification:** आपके पास विजिट से ठीक पहले WhatsApp / SMS Reminder पहुँच जाएगा।"
        )
        return response

    # ========================================================
    # SECTION 92 : POST-ADMISSION BATCH SETUP HANDLER
    # ========================================================

    def handle_post_admission_batch_setup(self):
        """
        Admission पूरा होने पर Student को उसका Batch allocations और Welcome Message देना
        """
        self.current_stage = "post_admission_complete"
        batch_details = self.handle_batch_allocation()

        response = (
            f"🌟 **Admission Confirmed & Batch Allotted!**\n\n"
            f"{batch_details}\n\n"
            f"आपकी Welcome Kit और ID Card आपके First Day पर Center से उपलब्ध करा दिया जाएगा।"
        )
        return response

    # ========================================================
    # SECTION 93 : MANUAL REMINDER TRIGGER FOR COUNSELLORS
    # ========================================================

    def trigger_manual_reminder(self):
        """
        अगर Counselor या Admin खुद मैन्युअली स्टूडेंट को रिमाइंडर भेजना चाहे
        """
        if self.demo_booked:
            return self.schedule_automated_reminder("DEMO")
        elif self.visit_scheduled:
            return self.schedule_automated_reminder("VISIT")
        else:
            return self.schedule_automated_reminder("GENERAL")

    # ========================================================
    # SECTION 94 : BATCH SLOT AVAILABILITY CHECKER
    # ========================================================

    def check_batch_availability(self, batch_key):
        """
        चेक करना कि चुने गए Batch में Seats ख़ाली हैं या नहीं
        """
        # डिफॉल्ट रूप से बैचेस उपलब्ध रहेंगे
        if batch_key in self.BATCH_SCHEDULE_DATA:
            return True, f"{batch_key} Batch में Seats उपलब्ध हैं।"
        return False, "चुना गया Batch टाइम उपलब्ध नहीं है।"

    # ========================================================
    # SECTION 95 : POST-BOOKING STAGE CONTROLLER
    # ========================================================

    def process_post_booking_stages(self, cleaned_msg):
        """
        Post-Booking / Post-Admission स्टेज की बातचीत संभालने वाला कंट्रोलर
        """
        if self.current_stage == "batch_assigned":
            return (
                f"**{self.student.name} जी**, आपका Batch और Timing पहले ही Set हो चुका है।\n"
                f"क्या आप Center के Google Maps Location का Link चाहते हैं?"
            )
        elif self.current_stage == "post_admission_complete":
            return (
                f"**{self.student.name} जी**, आपका Admission और Batch ऑलॉटमेंट पूरा हो चुका है। "
                f"हम आपकी पहली Class में आपसे मिलते हैं!"
            )
        return None
    
