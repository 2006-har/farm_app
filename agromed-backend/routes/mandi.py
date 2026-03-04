from flask import Blueprint, request, jsonify
from extensions import mysql

mandi_bp = Blueprint("mandi", __name__)

@mandi_bp.route("/add", methods=["POST"])
def add_mandi():
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute(
        "INSERT INTO mandi (mandi_name, district) VALUES (%s, %s)",
        (data["mandi_name"], data["district"])
    )
    mysql.connection.commit()

    return jsonify({"message": "Mandi added"})


@mandi_bp.route("/prices", methods=["GET"])
def view_prices():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM mandi_prices")
    prices = cursor.fetchall()
    return jsonify(prices)