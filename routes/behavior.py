from flask import Blueprint, request, jsonify
from db import mysql
behavior_bp = Blueprint("behavior", __name__)

@behavior_bp.route("/behavior", methods=["POST"])
def add_behavior():

    data = request.json

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO BehaviorLogs
        (Animal_ID, Behavior_Type, Observation, Date)
        VALUES (%s,%s,%s,%s)
    """,(data["animal_id"],data["behavior_type"],
         data["observation"],data["date"]))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Behavior log added"})