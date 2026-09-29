from ultralytics import YOLO
import cv2
import time
import os
from collections import defaultdict

os.makedirs('screenshots', exist_ok=True)

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
prev_time = 0

# Crowd density threshold
CROWD_THRESHOLD = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # Object tracking
    results = model.track(frame, persist=True)
    annotated_frame = results[0].plot()

    # Count objects
    object_counts = defaultdict(int)
    for box in results[0].boxes:
        cls = int(box.cls[0])
        object_counts[model.names[cls]] += 1

    # Crowd density alert
    person_count = object_counts.get('person', 0)
    if person_count > CROWD_THRESHOLD:
        cv2.putText(annotated_frame, "CROWD ALERT!", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        filename = f"screenshots/crowd_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        print(f"🚨 Crowd detected: {person_count} people")

    # Display info
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    y_pos = 70
    for obj, count in object_counts.items():
        cv2.putText(annotated_frame, f"{obj}: {count}", (10, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        y_pos += 35

    cv2.imshow("AI Tracker", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
