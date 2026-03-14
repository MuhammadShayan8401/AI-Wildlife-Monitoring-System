from flask import Blueprint, jsonify
from db import mysql

behavior_logs_bp = Blueprint("behavior_logs", __name__)

@behavior_logs_bp.route("/behavior-logs", methods=["GET"])
def behavior_logs():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT a.Name, a.Species, b.Behavior_Type, b.Date
    FROM BehaviorLogs b
    JOIN Animals a
    ON a.Animal_ID = b.Animal_ID
    ORDER BY b.Date DESC
    LIMIT 20
    """)

    logs = cur.fetchall()
    cur.close()

    return jsonify(logs)
