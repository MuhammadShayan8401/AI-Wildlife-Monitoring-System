from flask import Blueprint, jsonify
from db import mysql

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts", methods=["GET"])
def get_alerts():

    cur = mysql.connection.cursor()

    # High temperature enclosures
    cur.execute("""
        SELECT Enclosure_ID, Location, Temperature
        FROM Enclosures
        WHERE Temperature > 35
    """)
    high_temp = cur.fetchall()

    # Low humidity enclosures
    cur.execute("""
        SELECT Enclosure_ID, Location, Humidity
        FROM Enclosures
        WHERE Humidity < 30
    """)
    low_humidity = cur.fetchall()

    cur.close()

    return jsonify({
        "high_temperature_alerts": high_temp,
        "low_humidity_alerts": low_humidity
    })