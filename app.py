from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

conversation = [{"role": "system", "content": "You are a helpful assistant."}]

# In-memory user store for demonstration
users = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username in users:
        return jsonify({"error": "User already exists"}), 409
    users[username] = password
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    # For demonstration, check against in-memory users
    if username in users and users[username] == password:
        return jsonify({"token": "dummy-token-for-" + username})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/chat", methods=["POST"])
def chat():
    if not request.json or "message" not in request.json:
        return jsonify({"reply": "Error: No message provided."})

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
        error_message = str(e)
        if "'message'" in error_message:
            # Extract the message part from the error string
            import re
            match = re.search(r"'message': '([^']+)'", error_message)
            if match:
                reply = match.group(1)
            else:
                reply = "An error occurred."
        else:
            reply = "An error occurred."

    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)
