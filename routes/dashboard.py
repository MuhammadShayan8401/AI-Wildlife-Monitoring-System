from flask import Blueprint, jsonify
from db import mysql

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    cur = mysql.connection.cursor()

    # Total animals
    cur.execute("SELECT COUNT(*) FROM Animals")
    total_animals = cur.fetchone()[0]

    # Sick animals
    cur.execute("SELECT COUNT(*) FROM Animals WHERE Health_Status='Sick'")
    sick_animals = cur.fetchone()[0]

    # Healthy animals
    cur.execute("SELECT COUNT(*) FROM Animals WHERE Health_Status='Healthy'")
    healthy_animals = cur.fetchone()[0]

    # Total enclosures
    cur.execute("SELECT COUNT(*) FROM Enclosures")
    total_enclosures = cur.fetchone()[0]

    # Species distribution
    cur.execute("""
        SELECT Species, COUNT(*) 
        FROM Animals 
        GROUP BY Species
    """)
    species_data = cur.fetchall()
    species_distribution = {row[0]: row[1] for row in species_data}

    # AI Stress events per animal (Moderate + High)
    cur.execute("""
        SELECT a.Name, a.Species, COUNT(b.Log_ID) AS stress_events
        FROM Animals a
        LEFT JOIN BehaviorLogs b
            ON a.Animal_ID = b.Animal_ID
            AND b.Behavior_Type IN ('MODERATE_STRESS','HIGH_STRESS')
        GROUP BY a.Animal_ID
    """)
    stress_data = cur.fetchall()
    stress_per_animal = {row[0]: {"species": row[1], "stress_events": row[2]} for row in stress_data}

    # High stress events per enclosure
    cur.execute("""
        SELECT e.Location, COUNT(b.Log_ID) AS high_stress_events
        FROM Enclosures e
        LEFT JOIN Animals a ON a.Enclosure_ID = e.Enclosure_ID
        LEFT JOIN BehaviorLogs b
            ON a.Animal_ID = b.Animal_ID
            AND b.Behavior_Type='HIGH_STRESS'
        GROUP BY e.Enclosure_ID
    """)
    enclosure_data = cur.fetchall()
    high_stress_per_enclosure = {row[0]: row[1] for row in enclosure_data}

    cur.close()

    return jsonify({
        "total_animals": total_animals,
        "sick_animals": sick_animals,
        "healthy_animals": healthy_animals,
        "total_enclosures": total_enclosures,
        "species_distribution": species_distribution,
        "stress_per_animal": stress_per_animal,
        "high_stress_per_enclosure": high_stress_per_enclosure
    })