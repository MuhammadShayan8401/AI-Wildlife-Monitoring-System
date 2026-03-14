from flask import Blueprint, jsonify
from db import mysql

stress_bp = Blueprint("stress", __name__)

@stress_bp.route("/stress-animals", methods=["GET"])
def stress_animals():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT a.Name, a.Species, COUNT(b.Log_ID) AS stress_events
        FROM Animals a
        JOIN BehaviorLogs b ON a.Animal_ID = b.Animal_ID
        WHERE b.Behavior_Type='Stress'
        GROUP BY a.Animal_ID
    """)

    data = cur.fetchall()
    cur.close()

    return jsonify(data)