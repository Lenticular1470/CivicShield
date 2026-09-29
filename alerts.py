from ultralytics import YOLO
import cv2
import time
import pyttsx3
import os
from datetime import datetime

os.makedirs('screenshots', exist_ok=True)

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

engine = pyttsx3.init()
engine.setProperty('rate', 150)

last_alert_time = 0
alert_cooldown = 5

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)
    current_hour = datetime.now().hour

    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            # Intruder detection after 10 PM
            if label == "person" and current_hour >= 22:
                current_time = time.time()
                
                if current_time - last_alert_time > alert_cooldown:
                    filename = f"screenshots/intruder_{int(time.time())}.png"
                    cv2.imwrite(filename, frame)

                    engine.say("Warning! Intruder detected")
                    engine.runAndWait()

                    last_alert_time = current_time
                    print(f"🚨 INTRUDER ALERT! Screenshot: {filename}")

    annotated_frame = results[0].plot()

    cv2.imshow("Alert System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
