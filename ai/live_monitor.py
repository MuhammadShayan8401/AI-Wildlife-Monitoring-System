import cv2
import numpy as np
from db import mysql

# Stress threshold
STRESS_THRESHOLD = 50000

def log_behavior(animal_id, behavior, observation):

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
        INSERT INTO BehaviorLogs (Animal_ID, Behavior_Type, Observation, Date)
        VALUES (%s,%s,%s,NOW())
        """, (animal_id, behavior, observation))

        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print("Database Error:", e)


def run_live_monitor(animal_id=5):

    cap = cv2.VideoCapture(0)

    ret, prev_frame = cap.read()

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    print("Starting AI Wildlife Monitoring...")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Frame difference (movement detection)
        diff = cv2.absdiff(prev_gray, gray)

        movement_score = np.sum(diff)

        prev_gray = gray

        if movement_score > STRESS_THRESHOLD:

            behavior = "Stress"
            color = (0,0,255)

            log_behavior(animal_id, "Stress", "High movement detected")

        else:

            behavior = "Normal"
            color = (0,255,0)

        cv2.putText(
            frame,
            f"Behavior: {behavior}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Movement Score: {int(movement_score)}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.imshow("AI Wildlife Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
