from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

conversation = [{"role": "system", "content": "You are a helpful assistant."}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    conversation.append({"role": "user", "content": user_message})

    try:
        # Remove type enforcement to avoid import error
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        reply = response.choices[0].message.content
        if reply is None:
            reply = "Error: No content in response"
        else:
            reply = reply.strip()
    except Exception as e:
        reply = f"Error: {e}"

    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
