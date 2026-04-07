# TransiTrack
# 🚌 AI-Based Smart Bus Monitoring System

## 📌 Overview
This project is an AI-powered system that automatically detects bus numbers using a camera and OCR (EasyOCR). It logs bus arrival details into a cloud database (Supabase) and displays them on a live dashboard.

---

## 🚀 Features
- 🎥 Real-time camera detection
- 🔍 OCR-based number plate recognition
- ☁️ Cloud storage using Supabase
- 📊 Live dashboard (Flask)
- ⏰ On-time / Late status detection
- 🚨 Violation tracking

---

## 🧠 Tech Stack
- Python
- OpenCV
- EasyOCR
- Flask
- Supabase (Database)

---

## ⚙️ How It Works
1. Camera captures bus
2. OCR detects number plate
3. System checks timing (before/after 8:50 AM)
4. Data is stored in Supabase
5. Dashboard displays live updates

---

## 🖥️ Run Locally

### 1. Clone repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
