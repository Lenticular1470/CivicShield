# 🚀 AI Smart Surveillance System

## 🔹 Core Features

✅ **Real-time Object Detection** - Camera se objects detect honge  
✅ **Object Tracking** - Har object ko unique ID milegi  
✅ **Object Counting** - Screen par live count dikhega  
✅ **Screenshot Capture** - Auto save on detection  
✅ **Voice Alert** - Speaker se warning  
✅ **Detection Logs** - CSV file me record  

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🎯 Usage

### Run Main System
```bash
python main.py
```

**Controls:**
- Press **Q** to quit
- Press **S** for manual screenshot

---

## 🔹 System Flow

```
Camera
  ↓
AI detect object
  ↓
Screenshot save
  ↓
Voice alert
  ↓
Log file save
```

---

## 📊 Output Examples

### Screen Display:
```
FPS: 30
Persons: 2
Mobiles: 1
Bottles: 3
```

### Screenshot:
```
screenshots/person_1745.png
screenshots/mobile_1746.png
```

### Log File:
```
Time        Object      Confidence
10:32 PM    Person      0.94
10:34 PM    Mobile      0.88
10:35 PM    Person      0.91
```

---

## 🔥 Technologies

- Python
- OpenCV
- YOLOv8
- NumPy
- Pandas
- pyttsx3

---

## 💼 Project Name

**AI Smart Surveillance System**

Real-time object detection, tracking, and intelligent monitoring using YOLOv8 and OpenCV.

---

Made with ❤️ for AI Learning
