from flask import Blueprint, request, jsonify
from extensions import mysql

crops_bp = Blueprint("crops", __name__, url_prefix="/crops")

# -------------------------------
# List all crops
# -------------------------------
@crops_bp.route("/list", methods=["GET"])
def list_crops():
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crops")
    crops = cursor.fetchall()
    cursor.close()
    return jsonify(crops), 200


# -------------------------------
# Get a single crop by ID
# -------------------------------
@crops_bp.route("/<int:crop_id>", methods=["GET"])
def get_crop(crop_id):
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM crops WHERE crop_id = %s", (crop_id,))
    crop = cursor.fetchone()
    cursor.close()
    if not crop:
        return jsonify({"message": "Crop not found"}), 404
    return jsonify(crop), 200


# -------------------------------
# Add a new crop
# -------------------------------
@crops_bp.route("/add", methods=["POST"])
def add_crop():
    data = request.json
    crop_name = data.get("crop_name")
    growth_duration = data.get("growth_duration")

    if not crop_name or growth_duration is None:
        return jsonify({"message": "crop_name and growth_duration are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO crops (crop_name, growth_duration) VALUES (%s, %s)",
        (crop_name, growth_duration)
    )
    mysql.connection.commit()
    crop_id = cursor.lastrowid
    cursor.close()
    return jsonify({"message": "Crop added", "crop_id": crop_id}), 201


# -------------------------------
# Update an existing crop
# -------------------------------
@crops_bp.route("/update/<int:crop_id>", methods=["PUT"])
def update_crop(crop_id):
    data = request.json
    crop_name = data.get("crop_name")
    growth_duration = data.get("growth_duration")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM crops WHERE crop_id = %s", (crop_id,))
    crop = cursor.fetchone()
    if not crop:
        cursor.close()
        return jsonify({"message": "Crop not found"}), 404

    cursor.execute(
        "UPDATE crops SET crop_name=%s, growth_duration=%s WHERE crop_id=%s",
        (crop_name, growth_duration, crop_id)
    )
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Crop updated"}), 200


# -------------------------------
# Delete a crop
# -------------------------------
@crops_bp.route("/delete/<int:crop_id>", methods=["DELETE"])
def delete_crop(crop_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM crops WHERE crop_id = %s", (crop_id,))
    crop = cursor.fetchone()
    if not crop:
        cursor.close()
        return jsonify({"message": "Crop not found"}), 404

    cursor.execute("DELETE FROM crops WHERE crop_id = %s", (crop_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Crop deleted"}), 200