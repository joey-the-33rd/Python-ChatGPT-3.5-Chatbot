from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Chat
import openai
import os

chat_bp = Blueprint("chat", __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    user_msg = data["message"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_msg}]
    )
    reply = response.choices[0].message.content.strip()

    new_chat = Chat(user_id=user_id, message=user_msg, reply=reply)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"reply": reply})

@chat_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.timestamp.desc()).limit(20).all()

    return jsonify([{
        "message": chat.message,
        "reply": chat.reply,
        "timestamp": chat.timestamp
    } for chat in chats])
