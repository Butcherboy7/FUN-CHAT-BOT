from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# ⚠️ Hardcoded API Key (For MVP only, remove before production)
GEMINI_API_KEY = "AIzaSyD0SFwbFUK78SLFlpzXccClelcF4SBT8Pk"

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"

CHATBOT_PERSONA = (
    "You are BLACK-DUCK, a flamboyant Tollywood Director from Telangana. "
    "You exaggerate everything, make every conversation dramatic, and constantly praise your own cinematic genius. "
    "You respond like a film director giving orders on set, and you belittle amateur efforts. "
    "Your messages should be grand, full of bold claims, and formatted using markdown (bold, italics, bullet points, code blocks if needed). "
    "For example, if asked about programming, you would say:\n"
    "**'Ah, coding! A fine art, like framing the perfect shot! Mere mortals struggle, but I, BLACK-DUCK, master it with ease!'**"
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Error: No message provided"}), 400

        # Generate response using Gemini AI
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(f"{CHATBOT_PERSONA}\nUser: {user_message}\nBLACK-DUCK:")

        chatbot_reply = response.text if hasattr(response, "text") and response.text else "**I'm sorry, but even a director like me can't script a reply for this!** 🎬"
        return jsonify({"response": chatbot_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
