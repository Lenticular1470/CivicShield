from ultralytics import YOLO
import cv2

# YOLO model load
model = YOLO("yolov8n.pt")

# camera open
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # object detection
    results = model(frame)

    # result draw
    annotated_frame = results[0].plot()

    cv2.imshow("AI Object Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
