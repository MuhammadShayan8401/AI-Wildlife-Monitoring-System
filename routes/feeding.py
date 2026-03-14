from flask import Blueprint, request, jsonify
from db import mysql
feeding_bp = Blueprint("feeding", __name__)

@feeding_bp.route("/feeding", methods=["POST"])
def add_feeding():

    data = request.json

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO FeedingSchedule
        (Animal_ID, Food_Type, Time, Caretaker)
        VALUES (%s,%s,%s,%s)
    """,(data["animal_id"],data["food_type"],
         data["time"],data["caretaker"]))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Feeding record added"})