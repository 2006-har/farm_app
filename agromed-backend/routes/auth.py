from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import mysql

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (data["name"], data["email"], data["password"], data.get("role", "farmer"))
    )
    mysql.connection.commit()

    return jsonify({"message": "User registered successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (data["email"], data["password"])
    )
    user = cursor.fetchone()

    if user:
        token = create_access_token(identity=data["email"])
        return jsonify(access_token=token)
    else:
        return jsonify({"message": "Invalid credentials"}), 401