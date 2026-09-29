import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

# Create screenshot folder
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Load YOLO model
model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # Run YOLO detection
    results = model(frame, stream=True)
    
    object_count = 0
    for result in results:
        boxes = result.boxes
        object_count = len(boxes)
        
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display FPS and object count
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f"Objects: {object_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Advanced Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save screenshot
        filename = f"screenshots/capture_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

cap.release()
cv2.destroyAllWindows()
