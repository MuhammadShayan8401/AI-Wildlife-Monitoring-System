from flask import Blueprint, request, jsonify
from db import mysql
enclosures_bp = Blueprint("enclosures", __name__)

@enclosures_bp.route("/enclosures", methods=["GET"])
def get_enclosures():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Enclosures")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


@enclosures_bp.route("/enclosures", methods=["POST"])
def add_enclosure():

    data = request.json

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO Enclosures
        (Location, Temperature, Humidity, Size)
        VALUES (%s,%s,%s,%s)
    """,(data["location"],data["temperature"],
         data["humidity"],data["size"]))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Enclosure added"})