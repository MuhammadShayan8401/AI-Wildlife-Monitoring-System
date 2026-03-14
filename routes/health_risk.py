from flask import Blueprint, jsonify
from db import mysql

risk_bp = Blueprint("risk", __name__)

@risk_bp.route("/health-risk", methods=["GET"])
def health_risk():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT a.Name, a.Species, COUNT(h.Record_ID) AS health_issues
        FROM Animals a
        JOIN HealthRecords h ON a.Animal_ID = h.Animal_ID
        GROUP BY a.Animal_ID
        HAVING COUNT(h.Record_ID) >= 1
    """)

    data = cur.fetchall()
    cur.close()

    return jsonify(data)