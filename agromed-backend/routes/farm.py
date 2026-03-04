from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql

farm_bp = Blueprint("farm", __name__)

@farm_bp.route("/add", methods=["POST"])
@jwt_required()
def add_farm():
    data = request.json
    user_email = get_jwt_identity()

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT user_id FROM users WHERE email=%s", (user_email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]

    cursor.execute(
        "INSERT INTO farms (user_id, farm_name, soil_type, acreage) VALUES (%s, %s, %s, %s)",
        (user_id, data["farm_name"], data["soil_type"], data["acreage"])
    )

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Farm added successfully"})


@farm_bp.route("/all", methods=["GET"])
@jwt_required()
def view_farms():
    user_email = get_jwt_identity()
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT user_id FROM users WHERE email=%s", (user_email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]

    cursor.execute(
        "SELECT farm_id, farm_name, soil_type, acreage FROM farms WHERE user_id=%s",
        (user_id,)
    )

    farms = cursor.fetchall()
    cursor.close()

    result = []
    for farm in farms:
        result.append({
            "farm_id": farm[0],
            "farm_name": farm[1],
            "soil_type": farm[2],
            "acreage": float(farm[3])
        })

    return jsonify(result)


@farm_bp.route("/delete/<int:farm_id>", methods=["DELETE"])
@jwt_required()
def delete_farm(farm_id):
    user_email = get_jwt_identity()
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT user_id FROM users WHERE email=%s", (user_email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]

    cursor.execute(
        "DELETE FROM farms WHERE farm_id=%s AND user_id=%s",
        (farm_id, user_id)
    )

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Farm deleted successfully"})
@farm_bp.route("/update/<int:farm_id>", methods=["PUT"])
@jwt_required()
def update_farm(farm_id):
    data = request.json
    user_email = get_jwt_identity()
    cursor = mysql.connection.cursor()

    # Get user_id
    cursor.execute("SELECT user_id FROM users WHERE email=%s", (user_email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user[0]

    # Update only if farm belongs to this user
    cursor.execute(
        """
        UPDATE farms
        SET farm_name=%s, soil_type=%s, acreage=%s
        WHERE farm_id=%s AND user_id=%s
        """,
        (data["farm_name"], data["soil_type"], data["acreage"], farm_id, user_id)
    )

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Farm updated successfully"})