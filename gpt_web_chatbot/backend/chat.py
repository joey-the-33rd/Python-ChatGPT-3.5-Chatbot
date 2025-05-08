from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from gpt_web_chatbot.backend.models import db, Chat
import openai
import os


chat_bp = Blueprint("chat", __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    """
    Handle chat interactions with OpenAI's GPT model.

    This endpoint is protected by JWT authentication and handles POST requests
    containing a user message. It communicates with OpenAI's API to generate
    a chatbot response using the "gpt-3.5-turbo" model. If this model is not
    available, it falls back to using the "text-davinci-003" engine.

    The conversation, including user messages and AI-generated replies, is
    stored in the database associated with the user's identity.

    Returns:
        JSON response containing the AI-generated reply.
    """

    user_id = get_jwt_identity()
    data = request.get_json()
    user_msg = data["message"]

    # Use openai.ChatCompletion if available, else fallback to Completion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}],
        )
        reply = response.choices[0].message.content.strip()
    except AttributeError:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_msg,
            max_tokens=150,
        )
        reply = response.choices[0].text.strip()

    from typing import cast
    from gpt_web_chatbot.backend.models import Chat as ChatModel

    new_chat: ChatModel = cast(
        ChatModel,
        Chat(user_id=user_id, message=user_msg, reply=reply)  # type: ignore[arg-type]
    )
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"reply": reply})


@chat_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    """
    Retrieve chat history for the authenticated user.

    This endpoint is protected by JWT authentication and handles GET requests.
    It fetches the most recent chat messages and their corresponding replies
    for the currently authenticated user, limited to the latest 20 entries,
    sorted by the timestamp in descending order.

    Returns:
        JSON response containing a list of chat messages, each with the
        message content, AI-generated reply, and timestamp.
    """

    user_id = get_jwt_identity()
    chats = (
        Chat.query.filter_by(user_id=user_id)
        .order_by(Chat.timestamp.desc())
        .limit(20)
        .all()
    )

    return jsonify(
        [
            {
                "message": chat.message,
                "reply": chat.reply,
                "timestamp": chat.timestamp,
            }
            for chat in chats
        ]
    )
