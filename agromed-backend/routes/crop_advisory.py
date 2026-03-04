from flask import Blueprint, request, jsonify
from extensions import mysql

advisory_bp = Blueprint("advisory", __name__, url_prefix="/advisory")

# -------------------------------
# Get advisory for a specific crop
# -------------------------------
@advisory_bp.route("/<int:crop_id>", methods=["GET"])
def get_advisory(crop_id):
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.crop_name, a.growth_stage, a.irrigation_days, 
               a.pesticide_name, a.dosage_per_acre
        FROM crop_advisory a
        JOIN crops c ON a.crop_id = c.crop_id
        WHERE a.crop_id = %s
    """, (crop_id,))
    advisory = cursor.fetchall()
    cursor.close()
    if not advisory:
        return jsonify({"message": "No advisory found for this crop"}), 404
    return jsonify(advisory), 200


# -------------------------------
# Add new advisory
# -------------------------------
@advisory_bp.route("/add", methods=["POST"])
def add_advisory():
    data = request.json
    crop_id = data.get("crop_id")
    growth_stage = data.get("growth_stage")
    irrigation_days = data.get("irrigation_days")
    pesticide_name = data.get("pesticide_name")
    dosage_per_acre = data.get("dosage_per_acre")

    if not all([crop_id, growth_stage, irrigation_days]):
        return jsonify({"message": "crop_id, growth_stage, and irrigation_days are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO crop_advisory (crop_id, growth_stage, irrigation_days, pesticide_name, dosage_per_acre) "
        "VALUES (%s, %s, %s, %s, %s)",
        (crop_id, growth_stage, irrigation_days, pesticide_name, dosage_per_acre)
    )
    mysql.connection.commit()
    advisory_id = cursor.lastrowid
    cursor.close()
    return jsonify({"message": "Advisory added", "advisory_id": advisory_id}), 201