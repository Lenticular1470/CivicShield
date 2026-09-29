from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import pandas as pd
import os
from collections import defaultdict

app = Flask(__name__)
model = YOLO("yolov8n.pt")

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    log_file = "logs/detection_log.csv"
    stats = {"total_detections": 0, "persons": 0, "weapons": 0}
    
    if os.path.exists(log_file):
        data = pd.read_csv(log_file)
        stats["total_detections"] = len(data)
        stats["persons"] = len(data[data['object'] == 'person'])
        stats["weapons"] = len(data[data['object'].isin(['knife', 'scissors'])])
        table_html = data.to_html(index=False, border=0, classes='table')
    else:
        table_html = "<p>No logs available</p>"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Surveillance Dashboard</title>
        <style>
            body {{ font-family: Arial; background: #1a1a1a; color: white; padding: 20px; }}
            h1 {{ color: #00ff00; text-align: center; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-box {{ background: #2a2a2a; padding: 20px; border-radius: 10px; text-align: center; }}
            .stat-box h2 {{ color: #00ff00; margin: 0; }}
            img {{ border: 3px solid #00ff00; border-radius: 10px; max-width: 90%; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #00ff00; padding: 12px; text-align: left; }}
            th {{ background: #00ff00; color: black; }}
        </style>
    </head>
    <body>
        <h1>🚀 AI Surveillance & Threat Detection Platform</h1>
        <div class="stats">
            <div class="stat-box"><h2>{stats['total_detections']}</h2><p>Total Detections</p></div>
            <div class="stat-box"><h2>{stats['persons']}</h2><p>Persons Detected</p></div>
            <div class="stat-box"><h2>{stats['weapons']}</h2><p>Weapon Alerts</p></div>
        </div>
        <h2 style="color:#00ff00;">Live Camera Feed</h2>
        <img src="/video_feed" alt="Live Feed">
        <h2 style="color:#00ff00;">Detection History</h2>
        {table_html}
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("🌐 Dashboard running at: http://127.0.0.1:5000")
    app.run(debug=True)
