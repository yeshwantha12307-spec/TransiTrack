from flask import Flask, render_template
import requests

app = Flask(__name__)

SUPABASE_URL = "https://yqlerrucbdjkqiyfrjbj.supabase.co/rest/v1/bus_log"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxbGVycnVjYmRqa3FpeWZyamJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MTc5NTcsImV4cCI6MjA5MDI5Mzk1N30.8edwaC2-PEKYlTgzAZcl1MJgdR73Lq7aOBDSmIJGMDo"

headers = {
    "apikey": API_KEY,
    "Authorization": "Bearer " + API_KEY
}

@app.route("/")
def home():
    try:
        res = requests.get(SUPABASE_URL + "?select=*&order=arrival_time.desc", headers=headers)
        data = res.json()
    except Exception as e:
        print("Error:", e)
        data = []

    return render_template("index.html", buses=data)

if __name__ == "__main__":
    app.run(debug=True)