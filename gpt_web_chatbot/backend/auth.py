from flask import Blueprint, request, jsonify
from typing import Any, Optional, TypedDict, cast
from gpt_web_chatbot.backend.models import db, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

class RegisterRequest(TypedDict):
    username: str
    password: str

class LoginRequest(TypedDict):
    username: str
    password: str


@auth.route("/register", methods=["POST"])
def register() -> Any:
    data: Optional[dict] = request.get_json()
    if not data:
        return jsonify({"msg": "Invalid request"}), 400

    data_typed = cast(RegisterRequest, data)
    username = data_typed.get("username")
    password_raw = data_typed.get("password")

    if not isinstance(username, str) or not isinstance(password_raw, str):
        return jsonify({"msg": "Invalid username or password"}), 400

    password = generate_password_hash(password_raw)  # type: ignore

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    user = User(username=username, password=password)  # type: ignore[arg-type]
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201


@auth.route("/login", methods=["POST"])
def login() -> Any:
    data: Optional[dict] = request.get_json()
    if not data:
        return jsonify({"msg": "Invalid request"}), 400

    data_typed = cast(LoginRequest, data)
    username = data_typed.get("username")
    password_raw = data_typed.get("password")

    if not isinstance(username, str) or not isinstance(password_raw, str):
        return jsonify({"msg": "Invalid username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password_raw):  # type: ignore
        token = create_access_token(identity=user.id)  # type: ignore
        return jsonify({"token": token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401
