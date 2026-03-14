import cv2
import numpy as np
from datetime import datetime
from db import mysql

# ------------------------------
# MOVEMENT DETECTION
# ------------------------------
def detect_movement(video_path, show_video=False):
    cap = cv2.VideoCapture(video_path)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    movement_count = 0

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Lower threshold for testing
                continue
            movement_count += 1
            if show_video:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x,y), (x+w,y+h), (0,255,0), 2)

        if show_video:
            cv2.imshow("Animal Monitoring", frame1)
            if cv2.waitKey(40) == 27:
                break

        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break

    cap.release()
    cv2.destroyAllWindows()
    return movement_count

# ------------------------------
# STRESS CLASSIFICATION
# ------------------------------
def detect_stress(movement_count, high_threshold=300, moderate_threshold=150):
    if movement_count > high_threshold:
        return "HIGH_STRESS"
    elif movement_count > moderate_threshold:
        return "MODERATE_STRESS"
    else:
        return "NORMAL"

# ------------------------------
# LOG STRESS TO DATABASE
# ------------------------------
def log_stress(animal_id, stress_level, session_tag=None):
    try:
        cursor = mysql.connection.cursor()
        # Check if Animal_ID exists, pick first one if not
        cursor.execute("SELECT Animal_ID, Name FROM Animals WHERE Animal_ID=%s", (animal_id,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute("SELECT Animal_ID, Name FROM Animals LIMIT 1")
            row = cursor.fetchone()
            if row is None:
                print("No animals in database. Skipping log.")
                return
        animal_id, animal_name = row

        # Optional session_tag to avoid duplicate logs per session
        if session_tag:
            cursor.execute("""
                SELECT 1 FROM BehaviorLogs 
                WHERE Animal_ID=%s AND Observation LIKE %s
            """, (animal_id, f"%{session_tag}%"))
            if cursor.fetchone():
                print("Log for this session already exists. Skipping duplicate.")
                return

        observation = f"AI detected {stress_level} movement pattern"
        if session_tag:
            observation += f" | Session: {session_tag}"

        cursor.execute("""
            INSERT INTO BehaviorLogs
            (Animal_ID, Behavior_Type, Observation, Date)
            VALUES (%s,%s,%s,%s)
        """, (animal_id, stress_level, observation, datetime.now()))

        # Insert into Alerts table if HIGH_STRESS
        if stress_level == "HIGH_STRESS":
            cursor.execute("""
                INSERT INTO Alerts (Animal_ID, Type, Message, Date)
                VALUES (%s, %s, %s, %s)
            """, (animal_id, "Stress", f"{animal_name} is under HIGH stress!", datetime.now()))

        mysql.connection.commit()
        cursor.close()
        print(f"Logged {stress_level} for Animal_ID {animal_id}")

    except Exception as e:
        print("Database Error:", e)

# ------------------------------
# COMPLETE AI PIPELINE
# ------------------------------
def analyze_video(video_path, animal_id=None, show_video=False, session_tag=None):
    movement = detect_movement(video_path, show_video)
    stress_level = detect_stress(movement)
    log_stress(animal_id, stress_level, session_tag)
    return {
        "animal_id": animal_id,
        "movement_score": movement,
        "stress_level": stress_level
    }