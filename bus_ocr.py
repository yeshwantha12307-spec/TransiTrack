import cv2
import easyocr
import re
from datetime import datetime
import requests
import json   # 🔥 MUST

SUPABASE_URL = "https://yqlerrucbdjkqiyfrjbj.supabase.co/rest/v1/bus_log"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxbGVycnVjYmRqa3FpeWZyamJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MTc5NTcsImV4cCI6MjA5MDI5Mzk1N30.8edwaC2-PEKYlTgzAZcl1MJgdR73Lq7aOBDSmIJGMDo"

headers = {
    "apikey": API_KEY,
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Prefer": "return=representation"
}

reader = easyocr.Reader(['en'])
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

pattern = r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}"

print("Camera running...")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = reader.readtext(frame)

    for (bbox, text, prob) in results:
        text = text.replace(" ", "").upper()

        if re.match(pattern, text):

            now = datetime.now()
            expected_time = now.replace(hour=8, minute=50, second=0, microsecond=0)

            status = "ON TIME" if now <= expected_time else "LATE"
            violation = "YES" if status == "LATE" else "NO"
            reason = "Bus arrived late" if status == "LATE" else "On time"

            data = {
    "bus_number": text,
    "arrival_time": now.isoformat(),
    "status": status,
    "reason": reason,
    "confidence": float(prob),
    "violation": violation,
    "exit_time": None
}
            try:
                res = requests.post(SUPABASE_URL, headers=headers, data=json.dumps(data))
                print("Status:", res.status_code)
                print("Response:", res.text)
            except Exception as e:
                print("Error:", e)

    cv2.imshow("Bus OCR", frame)

    if cv2.waitKey(1) == 27:
        print("Camera stopped")
        break

cap.release()
cv2.destroyAllWindows()