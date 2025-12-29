# 🏋️ Gym Form Correction AI

A **production-grade computer vision application** that analyzes exercise form in real time using a webcam or video input. The system detects body posture, counts repetitions, and provides corrective feedback for common gym exercises such as squats, push-ups, and deadlifts.

Built with **Python, MediaPipe, and OpenCV**, this project demonstrates clean architecture, real-time pose estimation, and scalable design suitable for deployment or further ML enhancement.

---

## 🚀 Features

* ✅ Real-time pose estimation using MediaPipe
* ✅ Exercise-specific form analysis (Squat, Push-up, Deadlift)
* ✅ Rep counting with state tracking
* ✅ Live visual feedback overlay
* ✅ Modular, production-ready architecture
* ✅ Robust error handling for camera and pose detection

---

## 🧠 System Architecture

```
Camera / Video Input
        ↓
Pose Estimator (MediaPipe)
        ↓
Landmark Processing & Angle Calculation
        ↓
Exercise Analyzer (Rules / Logic)
        ↓
Rep Counter & Feedback Engine
        ↓
Live UI Overlay (OpenCV)
```

---

## 📁 Project Structure

```
image-recognition/
│── app/
│   ├── main.py            # Application entry point
│   ├── camera.py
│   └── config.py
│── pose/
│   ├── estimator.py       # MediaPipe pose wrapper
│   └── smoother.py
│
│── exercises/
│   ├── base.py            # Abstract exercise class
│   ├── squat.py           # Squat logic (angles, reps, feedback)
│   ├── deadlift.py
│   └── pushup.py
│
│── analysis/
│   └── angles.py          # Joint angle calculations
│
│── feedback/
│   ├── overlay.py         # UI text overlay helpers
│   └── messages.py
│       
│── tests/
│   ├── test_angles.py     # Unit tests
│   └── test_reps.py
│── requirements.txt
│── README.md
```

---

## 🛠️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/gym-form-ai.git
cd gym-form-ai
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

#### Intel Mac

```bash
pip install opencv-python mediapipe==0.10.12 numpy
```

#### Apple Silicon (M1/M2)

```bash
pip install opencv-python mediapipe-silicon==0.10.12 numpy
```

---

## ▶️ Running the App

From the **project root directory**:

```bash
python3 -m app.main
```

* Press **`q`** to exit the application
* Ensure your webcam is connected and accessible

---

## 🏋️ Supported Exercises

| Exercise | Features                                        |
| -------- | ----------------------------------------------- |
| Squat    | Rep counting, depth detection, posture feedback |
| Push-up  | (Planned)                                       |
| Deadlift | (Planned)                                       |

---

## 📊 Metrics Tracked

* Total repetitions
* Joint angles per rep
* Depth consistency
* Form warnings frequency

These metrics can be extended to generate **session reports** or **performance scores**.

---

## 🧪 Testing

Run unit tests from the root directory:

```bash
pytest tests/
```

---

## 🔮 Future Improvements

* 🔹 ML-based form scoring (Random Forest / LSTM)
* 🔹 Streamlit web dashboard
* 🔹 REST API with FastAPI
* 🔹 Mobile app frontend (React Native)
* 🔹 User profiles & workout history

---

## 🧠 Key Technical Concepts Demonstrated

* Real-time computer vision
* Human pose estimation
* Modular Python architecture
* State-based rep counting
* Noise handling & smoothing
* Production-level error handling

---

## 🏆 Resume Description

> Built a production-grade Gym Form Correction AI using Python, MediaPipe, and OpenCV that analyzes exercise posture in real time, counts repetitions, and provides corrective feedback through a modular, scalable architecture.

---

## 📜 License

MIT License

---

## 👤 Author

**Emanuel Poblano**
Computer Vision / Software Engineering Project
