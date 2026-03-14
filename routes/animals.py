from flask import Blueprint, request, jsonify
from db import mysql
animals_bp = Blueprint("animals", __name__)

# GET all animals
@animals_bp.route("/animals", methods=["GET"])
def get_animals():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Animals")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


# GET single animal
@animals_bp.route("/animals/<int:id>", methods=["GET"])
def get_animal(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Animals WHERE Animal_ID=%s", (id,))
    data = cur.fetchone()
    cur.close()

    return jsonify(data)


# ADD animal
@animals_bp.route("/animals", methods=["POST"])
def add_animal():
    data = request.json

    name = data["name"]
    species = data["species"]
    age = data["age"]
    gender = data["gender"]
    health = data["health_status"]
    enclosure = data["enclosure_id"]

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Animals 
        (Name, Species, Age, Gender, Health_Status, Enclosure_ID)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,(name,species,age,gender,health,enclosure))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Animal added successfully"})


# UPDATE animal
@animals_bp.route("/animals/<int:id>", methods=["PUT"])
def update_animal(id):

    data = request.json

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE Animals 
        SET Name=%s, Species=%s, Age=%s, Gender=%s, Health_Status=%s
        WHERE Animal_ID=%s
    """,(data["name"],data["species"],data["age"],
        data["gender"],data["health_status"],id))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Animal updated"})


# DELETE animal
@animals_bp.route("/animals/<int:id>", methods=["DELETE"])
def delete_animal(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Animals WHERE Animal_ID=%s",(id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Animal deleted"})