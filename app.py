import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
from Data.keywords import CRISIS_KEYWORDS

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key was not found. Please set it in your .env file.")


openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
def check_for_crisis(message):

    # Check if a message contains any crisis keywords.

    for keyword in CRISIS_KEYWORDS:
        if keyword in message.lower():
            return True
    return False

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if check_for_crisis(user_input):
        crisis_response = (
        "It sounds like you might be in a crisis. "
        "Please reach out to a trusted individual or contact an emergency hotline such as 988 in the US. "
        "You can also speak with a licensed mental health professional. Your safety matters."
    )
        print(f"Crisis detected: {user_input}")
        return jsonify({"reply": crisis_response})

    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        # "You are an empathetic assistant that provides supportive mental health advice. "
                        # "Always include the message: 'Disclaimer: I am not a licensed mental health professional. "
                        # "If you are in crisis, please seek help immediately.'"
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        assistant_reply = response.choices[0].message.content.strip()

        disclaimer = "\n\nDisclaimer: I am not a licensed mental health professional. If you are in crisis, please contact your local emergency services immediately."
        full_reply = f"{assistant_reply}{disclaimer}"
        return jsonify({"reply": full_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, I am having trouble processing that request right now."})

if __name__ == "__main__":
    app.run(debug=True)
