from flask import Blueprint, request, jsonify
from db import mysql
health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["POST"])
def add_health():

    data = request.json

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO HealthRecords
        (Animal_ID, Checkup_Date, Diagnosis, Treatment)
        VALUES (%s,%s,%s,%s)
    """,(data["animal_id"],data["date"],
         data["diagnosis"],data["treatment"]))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Health record added"})