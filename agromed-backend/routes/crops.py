from flask import Blueprint, request, jsonify
from extensions import mysql

crops_bp = Blueprint("crops", __name__)

# Add a new crop
@crops_bp.route("/add", methods=["POST"])
def add_crop():
    data = request.json
    crop_name = data.get("crop_name")
    growth_duration = data.get("growth_duration")

    if not crop_name or growth_duration is None:
        return jsonify({"error": "crop_name and growth_duration are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO crops (crop_name, growth_duration) VALUES (%s, %s)",
        (crop_name, growth_duration)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Crop added successfully"}), 201


# List all crops
@crops_bp.route("/list", methods=["GET"])
def list_crops():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT crop_id, crop_name, growth_duration FROM crops")
    crops = cursor.fetchall()
    cursor.close()

    result = []
    for crop in crops:
        result.append({
            "crop_id": crop[0],
            "crop_name": crop[1],
            "growth_duration": crop[2]
        })

    return jsonify(result)


# Update a crop
@crops_bp.route("/update/<int:crop_id>", methods=["PUT"])
def update_crop(crop_id):
    data = request.json
    crop_name = data.get("crop_name")
    growth_duration = data.get("growth_duration")

    if not crop_name or growth_duration is None:
        return jsonify({"error": "crop_name and growth_duration are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE crops SET crop_name=%s, growth_duration=%s WHERE crop_id=%s",
        (crop_name, growth_duration, crop_id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Crop updated successfully"})

# Delete a crop safely
@crops_bp.route("/delete/<int:crop_id>", methods=["DELETE"])
def delete_crop(crop_id):
    cursor = mysql.connection.cursor()
    try:
        # Step 1: Delete any dependent crop advisories
        cursor.execute("DELETE FROM crop_advisory WHERE crop_id=%s", (crop_id,))
        
        # Step 2: Delete the crop itself
        cursor.execute("DELETE FROM crops WHERE crop_id=%s", (crop_id,))
        
        mysql.connection.commit()
        return jsonify({"message": "Crop and related advisories deleted successfully"}), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()