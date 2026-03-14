import cv2
import numpy as np
from ultralytics import YOLO
from db import mysql

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

STRESS_THRESHOLD = 40000


def log_behavior(animal_id, behavior):

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
        INSERT INTO BehaviorLogs (Animal_ID, Behavior_Type, Observation, Date)
        VALUES (%s,%s,%s,NOW())
        """, (animal_id, behavior, "YOLO movement detection"))

        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print("Database error:", e)


def run_detection():

    cap = cv2.VideoCapture(0)

    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    print("AI Animal Monitoring Started")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # YOLO detection
        results = model(frame)

        for r in results:
            boxes = r.boxes

            for box in boxes:

                cls = int(box.cls[0])

                label = model.names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

                cv2.putText(
                    frame,
                    label,
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )

        # Movement detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(prev_gray, gray)

        movement_score = np.sum(diff)

        prev_gray = gray

        if movement_score > STRESS_THRESHOLD:

            behavior = "Stress"
            color = (0,0,255)

            log_behavior(5,"Stress")

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

        cv2.imshow("AI Wildlife Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_detection()
