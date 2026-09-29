# 🚀 CivicShield - AI Smart Surveillance & Threat Detection Platform

Advanced real-time AI-powered surveillance system using YOLOv8, OpenCV, and Python for intelligent monitoring, threat detection, and smart alerts.

## 🎯 Vision

Transform basic object detection into an intelligent security monitoring platform for smart buildings, campuses, and retail environments.

## 📋 Core AI Modules

✅ **Real-time Object Detection** - YOLOv8 powered detection  
✅ **Object Tracking** - Unique ID assignment and tracking  
✅ **Face Recognition** - Known/Unknown person identification  
✅ **Weapon Detection** - Knife and dangerous object detection  
✅ **Crowd Density Analysis** - People counting and crowd alerts  
✅ **Intruder Detection** - Restricted hours monitoring (22:00-06:00)  
✅ **Suspicious Activity Detection** - Behavioral analysis  
✅ **Voice Alert System** - Real-time audio warnings  
✅ **Telegram Notifications** - Mobile alerts with images  
✅ **Detection Logging** - CSV-based event logging  
✅ **Web Dashboard** - Live monitoring and analytics  

## 🛠️ Installation

### 1. Python Check
```bash
python --version
```

### 2. Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> Face recognition uses OpenCV's YuNet and SFace models. It does not require `dlib` or Visual Studio C++ Build Tools. The models download automatically on the first run, so an internet connection is needed once.

## 🎯 Usage

### 1. Camera Test
```bash
python camera_test.py
```

### 2. Basic Detection
```bash
python detect.py
```

### 3. Object Tracking with Crowd Analysis
```bash
python tracker.py
```
- Tracks objects with unique IDs
- Counts people in frame
- Alerts when crowd > 10 people

### 4. Face Recognition System
```bash
python face_recognition_module.py
```
**Setup:**
- If OpenCV is already installed, remove the standard package first: `python -m pip uninstall -y opencv-python`
- Install dependencies with `python -m pip install -r requirements.txt`
- Add known person images to `faces/`; supported formats are JPG, JPEG, and PNG
- Name each image `person_name.jpg`; that filename is shown for a match
- System will identify known vs unknown faces

### 5. Alert System (Weapon + Intruder Detection)
```bash
python alerts.py
```
**Features:**
- Detects weapons (knife, scissors)
- Intruder detection (22:00-06:00)
- Voice alerts
- Auto screenshot capture
- Event logging

### 6. Web Dashboard
```bash
python dashboard.py
```
Open browser: **http://127.0.0.1:5000**

**Features:**
- Live camera feed
- Detection statistics
- Event history
- Analytics panel

### 8. Main Surveillance System
```bash
python main.py
```
Complete system with all features

## ⌨️ Controls

- **Q** - Quit
- **S** - Save Screenshot (in some modules)

## 📦 Detected Objects

**Standard Objects:**
Person, Car, Bicycle, Motorcycle, Bus, Truck, Bottle, Cup, Mobile Phone, Laptop, Mouse, Keyboard, Chair, Sofa

**Weapons:**
Knife, Scissors

**Total:** 80+ object classes supported by YOLOv8

## 🎓 Project Structure
```
Real time object detection/
├── camera_test.py              # Camera verification
├── detect.py                   # Simple YOLO detection
├── track.py                    # Basic object tracking
├── tracker.py                  # Advanced tracking + crowd analysis
├── face_recognition_module.py  # Face recognition system
├── alerts.py                   # Weapon + intruder detection
├── dashboard.py                # Web dashboard (Flask)
├── main.py                     # Complete surveillance system
├── requirements.txt            # Dependencies
├── screenshots/                # Auto saved images
├── logs/                       # Detection logs (CSV)
├── faces/                      # Known faces database
├── models/                     # Downloaded YuNet and SFace models
└── README.md                   # Documentation
```

## 🔥 Technologies Used

- **Python 3.x** - Core programming language
- **OpenCV** - Computer vision library
- **YOLOv8 (Ultralytics)** - Object detection model
- **NumPy** - Numerical computing
- **pyttsx3** - Text-to-speech for voice alerts
- **Flask** - Web dashboard framework
- **OpenCV YuNet and SFace** - Face detection and recognition
- **Pandas** - Data logging and analysis

## 🎯 Use Cases

🎥 **CCTV Surveillance** - 24/7 monitoring  
👥 **Crowd Analysis** - Event management  
🚗 **Traffic Monitoring** - Vehicle tracking  
🛒 **Smart Retail Stores** - Customer analytics  
🏠 **Home Security** - Intruder detection  
🚨 **Threat Detection** - Weapon identification  
🏢 **Corporate Security** - Access control  
🎓 **Campus Safety** - Student monitoring  

## 🚨 Alert System

### Intruder Detection
- **Trigger:** Person detected between 22:00-06:00
- **Actions:** Screenshot + Voice alert + Log event

### Weapon Detection
- **Trigger:** Knife or dangerous object detected
- **Alert Level:** HIGH
- **Actions:** Screenshot + Voice alert + Log event

### Crowd Alert
- **Trigger:** More than 10 people detected
- **Actions:** Screenshot + On-screen warning

### Unknown Person
- **Trigger:** Face not in database
- **Actions:** Alert + Log event

## 📊 Detection Log Format

```csv
timestamp,object,confidence,camera_id
2024-03-10 22:01:12,person,0.94,CAM-1
2024-03-10 22:02:33,knife,0.87,CAM-1
2024-03-10 22:03:02,person,0.91,CAM-1
```

## 🌐 Web Dashboard Features

- **Live Camera Stream** - Real-time video feed
- **Detection Statistics** - Total detections, persons, weapons
- **Event History** - Timestamped detection log
- **Analytics Panel** - Visual data representation

## 💼 LinkedIn / Resume Title

**AI Smart Surveillance & Threat Detection Platform using YOLOv8, OpenCV and Python**

**Key Features:**
- Real-time object detection and tracking
- Face recognition system
- Weapon detection with high-priority alerts
- Crowd density analysis
- Intruder detection (restricted hours)
- Voice alert system
- Web-based monitoring dashboard
- Event logging and analytics

## 🔧 Configuration

### Crowd Threshold
Edit `tracker.py`:
```python
CROWD_THRESHOLD = 10  # Change to your requirement
```

### Restricted Hours
Edit `alerts.py`:
```python
if current_hour >= 22 or current_hour < 6:  # 22:00-06:00
```

### Alert Cooldown
Edit `alerts.py`:
```python
alert_cooldown = 5  # seconds between alerts
```

## 📝 Notes

- First run will download YOLOv8 model (~6MB)
- Face recognition requires dlib (may need Visual C++ on Windows)
- Web dashboard runs on port 5000 by default

## 🤝 Contributing

This is an educational project. Feel free to fork and enhance!

## 📄 License

MIT License - Free to use for learning and commercial purposes

---

**Made with ❤️ for AI Learning and Smart Security**

🔗 **Technologies:** Python | OpenCV | YOLOv8 | Flask | Deep Learning | Computer Vision
