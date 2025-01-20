import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai


# Load environment variables from .env
load_dotenv()

# Retrieve your API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OpenAI API key was not found. Please set it in your .env file.")

# Set up the OpenAI library with your API key
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/")
def index():
    # Make sure you have an index.html in your templates folder.
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    try:
        # Create a chat completion request using GPT-4
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
            max_tokens=150  # Adjust as necessary for your expected response length.
        )
        assistant_reply = response.choices[0].message.content.strip()
        # Append a final disclaimer if needed
        disclaimer = "\n\nDisclaimer: I am not a licensed mental health professional. If you are in crisis, please contact your local emergency services immediately."
        full_reply = f"{assistant_reply}{disclaimer}"
        return jsonify({"reply": full_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, I am having trouble processing that request right now."})

if __name__ == "__main__":
    app.run(debug=True)
