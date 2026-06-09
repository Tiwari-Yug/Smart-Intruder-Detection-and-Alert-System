# Smart Intruder Detection and Alert System

A real-time AI-powered security surveillance system that uses **Face Recognition** and **Computer Vision** to identify authorized individuals and detect intruders. When an unknown person is detected, the system automatically captures their image and sends an email alert with the evidence attached.

---

## 🚀 Features

* 🔍 Real-time face detection using webcam feed
* 👤 Recognition of authorized users from a preloaded dataset
* 🚨 Automatic intruder detection for unknown faces
* 📸 Intruder image capture and storage
* 📧 Email alert system with attached intruder image
* ⚡ Optimized frame processing for better performance
* 🎯 Adjustable face-matching tolerance to reduce false positives

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **Face Recognition (dlib)**
* **NumPy**
* **SMTP (Email Automation)**
* **Computer Vision**
* **Machine Learning**

---

## 📂 Project Structure

```text
project/
│
├── data/                  # Authorized users' images
├── intruders/             # Captured intruder images
├── proj_strict.py         # Main application
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

1. Load images of authorized users from the dataset.
2. Generate face encodings for all known individuals.
3. Start webcam video stream.
4. Detect and encode faces in real time.
5. Compare detected faces with stored encodings.
6. If a match is found:

   * Display the person's name.
7. If no match is found:

   * Mark the person as **Unknown**.
   * Capture and save the image.
   * Send an email alert with the captured image attached.

---

## 🧠 Face Recognition Pipeline

```text
Dataset Images
      ↓
Face Encoding
      ↓
Live Webcam Feed
      ↓
Face Detection
      ↓
Face Matching
      ↓
 ┌─────────────┬─────────────┐
 │ Known Face  │ Unknown Face│
 └─────────────┴─────────────┘
      ↓               ↓
 Display Name   Save Image
                     ↓
               Send Email Alert
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-intruder-detection.git
cd smart-intruder-detection
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📋 Requirements

Create a `requirements.txt` file:

```txt
face-recognition
opencv-python
numpy
dlib
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

### Dataset Path

Place images of authorized users inside:

```text
data/
```

Example:

```text
data/
├── John.jpg
├── Alice.jpg
└── Bob.jpg
```

The filename will be used as the recognized person's name.

### Email Configuration

Update the following variables in the code:

```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
recipient_email = "recipient@gmail.com"
```

> **Note:** Use a Gmail App Password instead of your regular Gmail password.

---

## ▶️ Run the Project

```bash
python proj_strict.py
```

Press:

```text
Q
```

or

```text
F
```

to exit the application.

---

## 📸 Sample Output

### Known User

```text
Name: John
Status: Authorized
```

### Unknown User

```text
Intruder detected!
Image saved successfully.
Email alert sent.
```

---

## 🔒 Security Features

* Real-time surveillance monitoring
* Automated evidence collection
* Email-based security notifications
* Reduced false matches using strict recognition thresholds
* Continuous monitoring through webcam feed

---

## 🎯 Future Enhancements

* SMS/WhatsApp alerts
* Cloud image storage
* Multi-camera support
* Attendance logging
* Web dashboard for monitoring
* Database integration
* Live mobile notifications

---

## 📈 Resume Highlights

* Developed a real-time face recognition surveillance system using OpenCV and Face Recognition.
* Implemented automated intruder detection and email alert mechanisms.
* Optimized recognition accuracy using customized face-matching thresholds.
* Applied computer vision techniques for security and monitoring applications.

---

## 👨‍💻 Author

**Your Name**

GitHub: `https://github.com/Tiwari-Yug`

---

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify it for educational and research purposes.
