from flask import Blueprint, request, jsonify
from extensions import mysql

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.route("/add", methods=["POST"])
def add_expense():
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute(
        "INSERT INTO expenses (farm_id, category, amount, expense_date) VALUES (%s, %s, %s, %s)",
        (data["farm_id"], data["category"], data["amount"], data["expense_date"])
    )
    mysql.connection.commit()

    return jsonify({"message": "Expense added"})


@expenses_bp.route("/total/<int:farm_id>", methods=["GET"])
def total_expense(farm_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE farm_id=%s",
        (farm_id,)
    )
    total = cursor.fetchone()
    return jsonify({"total_expense": total[0]})