from ultralytics import YOLO
import cv2
import time
import os
import pandas as pd
import pyttsx3
from collections import defaultdict
from datetime import datetime

# Setup
os.makedirs('screenshots', exist_ok=True)
os.makedirs('logs', exist_ok=True)

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

# Voice engine - Reinitialize with different driver
try:
    engine = pyttsx3.init('sapi5')  # Windows specific
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # Use first voice
    print("✅ Voice engine initialized (SAPI5)")
except Exception as e:
    print(f"❌ Voice engine error: {e}")
    engine = None

# Tracking
log_data = []
prev_time = 0
last_alert_time = {}  # Tracks last alert time per object

print("🚀 AI Smart Surveillance System Started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # Detection with tracking
    results = model.track(frame, persist=True)
    annotated_frame = results[0].plot()

    # Object counting
    object_counts = defaultdict(int)
    
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls]
        object_counts[label] += 1

        # Voice Alert for ALL detected objects (every 3 seconds per object)
        current_time = time.time()
        if label not in last_alert_time or (current_time - last_alert_time[label]) > 3:
            timestamp = int(time.time())
            filename = f"screenshots/{label.replace(' ', '_')}_{timestamp}.png"
            cv2.imwrite(filename, frame)
            
            # Voice alert - Dynamic for ALL objects
            if engine:
                try:
                    # Debug: Print label value
                    print(f"\n=== DEBUG INFO ===")
                    print(f"Class ID: {cls}")
                    print(f"Label from model: '{label}'")
                    print(f"Label type: {type(label)}")
                    print(f"Label length: {len(label)}")
                    
                    # Create alert message
                    alert_message = f"{label} detected"
                    print(f"Alert message: '{alert_message}'")
                    print(f"Message length: {len(alert_message)}")
                    print(f"==================\n")
                    
                    print(f"🔊 Speaking: {alert_message}")
                    
                    # Stop any previous speech
                    engine.stop()
                    
                    # Speak the message
                    engine.say(alert_message)
                    engine.runAndWait()
                    
                    print("✅ Voice alert completed")
                except Exception as e:
                    print(f"❌ Voice error: {e}")
            
            last_alert_time[label] = current_time
            print(f"📸 Screenshot: {filename}")
            print(f"✅ Detected: {label} (Confidence: {conf:.2f})")
            
            # Log entry
            log_data.append({
                "Time": datetime.now().strftime("%I:%M %p"),
                "Object": label,
                "Confidence": f"{conf:.2f}"
            })

    # Display FPS
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display object counts
    y_pos = 70
    for obj, count in object_counts.items():
        display_name = "Mobiles" if obj == "cell phone" else f"{obj.title()}s"
        cv2.putText(annotated_frame, f"{display_name}: {count}", (10, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        y_pos += 40

    cv2.imshow("AI Smart Surveillance System", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        filename = f"screenshots/manual_{int(time.time())}.png"
        cv2.imwrite(filename, frame)
        print(f"📸 Manual screenshot: {filename}")

cap.release()
cv2.destroyAllWindows()

# Save logs
if log_data:
    df = pd.DataFrame(log_data)
    log_file = f"logs/detection_log_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(log_file, index=False)
    print(f"✅ Logs saved: {log_file}")
    print("\n📊 Detection Summary:")
    print(df.to_string(index=False))
