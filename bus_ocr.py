import cv2
import easyocr
import re
from datetime import datetime
import requests
from twilio.rest import Client

# 🔥 SUPABASE
SUPABASE_URL = "https://yqlerrucbdjkqiyfrjbj.supabase.co/rest/v1/bus_log"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxbGVycnVjYmRqa3FpeWZyamJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MTc5NTcsImV4cCI6MjA5MDI5Mzk1N30.8edwaC2-PEKYlTgzAZcl1MJgdR73Lq7aOBDSmIJGMDo"

headers = {
    "apikey": API_KEY,
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json"
}

# 🔥 TWILIO
client = Client("ACd0f7a96b962ecbc134a4f9c81d76f1fd", "ac7cffaca8542a425e63375d896e7172")

TWILIO_NUMBER = "+17405677550"
COORDINATOR_NUMBER = "+918667468455"

# 🔥 NGROK URL
BASE_URL = "https://unsmouldering-else-captivatedly.ngrok-free.dev/reason?bus=TN45AB1234"

# 🔥 OCR
reader = easyocr.Reader(['en'])
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

pattern = r"[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}"

# 🔥 CONTROL
last_seen = {}
COOLDOWN = 5
EXIT_WINDOW = 30

print("Camera running... Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = reader.readtext(frame)

    for (_, text, prob) in results:
        text = text.replace(" ", "").upper()

        if re.match(pattern, text):

            now = datetime.now()

            # 🔥 COOLDOWN
            if text in last_seen:
                diff = (now - last_seen[text]).total_seconds()

                if diff < COOLDOWN:
                    continue

                # 🔴 EXIT
                if diff < EXIT_WINDOW:
                    url = SUPABASE_URL + f"?bus_number=eq.{text}&exit_time=is.null&order=arrival_time.desc&limit=1"
                    res = requests.get(url, headers=headers)

                    if res.status_code == 200 and len(res.json()) > 0:
                        row_id = res.json()[0]["id"]

                        update_url = SUPABASE_URL + f"?id=eq.{row_id}"
                        data = {
                            "exit_time": now.isoformat()
                        }

                        r = requests.patch(update_url, headers=headers, json=data)
                        print(f"🚪 EXIT UPDATED: {text}", r.status_code)

                    last_seen[text] = now
                    continue

            # 🟢 ENTRY
            data = {
                "bus_number": text,
                "arrival_time": now.isoformat(),
                "status": "LATE",
                "confidence": float(prob),
                "violation": "YES",
                "exit_time": None
            }

            r = requests.post(SUPABASE_URL, headers=headers, json=data)
            print(f"🟢 ENTRY SAVED: {text}", r.status_code)

            # 🔥 SEND SMS WITH LINK
            link = f"{BASE_URL}/reason?bus={text}"

            try:
                msg = client.messages.create(
                    body=f"""🚨 BUS ALERT

Bus: {text}
Status: LATE

Submit reason:
{link}
""",
                    from_=TWILIO_NUMBER,
                    to=COORDINATOR_NUMBER
                )
                print("📩 SMS SENT:", msg.sid)

            except Exception as e:
                print("SMS Error:", e)

            last_seen[text] = now

    cv2.imshow("Bus OCR", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()