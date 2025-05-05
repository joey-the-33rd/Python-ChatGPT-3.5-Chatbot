from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401
