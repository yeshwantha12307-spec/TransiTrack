from flask import Flask, request, render_template, render_template_string
import requests

app = Flask(__name__)

BUS_LOG_URL = "https://yqlerrucbdjkqiyfrjbj.supabase.co/rest/v1/bus_log"
REASON_URL = "https://yqlerrucbdjkqiyfrjbj.supabase.co/rest/v1/reason"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxbGVycnVjYmRqa3FpeWZyamJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ3MTc5NTcsImV4cCI6MjA5MDI5Mzk1N30.8edwaC2-PEKYlTgzAZcl1MJgdR73Lq7aOBDSmIJGMDoYOUR_API_KEY"

headers = {
    "apikey": API_KEY,
    "Authorization": "Bearer " + API_KEY,
    "Content-Type": "application/json"
}

# 🔥 DASHBOARD PAGE
@app.route("/")
def dashboard():
    res = requests.get(BUS_LOG_URL, headers=headers)
    data = res.json()

    return render_template("dashboard.html", buses=data)


# 🔥 FORM PAGE
@app.route("/reason")
def reason():
    bus = request.args.get("bus")

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bus Alert</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>

    <body class="bg-gray-900 text-white flex items-center justify-center h-screen">

        <div class="bg-gray-800 p-8 rounded-2xl shadow-xl w-96">

            <h2 class="text-2xl font-bold mb-4 text-red-400">
                🚨 Bus {{bus}} is Late
            </h2>

            <form action="/submit" method="post" class="space-y-4">

                <input type="hidden" name="bus" value="{{bus}}">

                <input 
                    type="text" 
                    name="reason"
                    placeholder="Enter reason..."
                    class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600"
                    required
                >

                <button 
                    class="w-full bg-red-500 hover:bg-red-600 p-3 rounded-lg font-bold">
                    Submit
                </button>

            </form>

        </div>

    </body>
    </html>
    """, bus=bus)


# 🔥 SAVE REASON
@app.route("/submit", methods=["POST"])
def submit():
    bus = request.form.get("bus")
    reason = request.form.get("reason")

    # 🔥 GET LATEST BUS LOG
    url = BUS_LOG_URL + f"?bus_number=eq.{bus}&order=arrival_time.desc&limit=1"
    res = requests.get(url, headers=headers)

    if res.status_code == 200 and len(res.json()) > 0:
        bus_log_id = res.json()[0]["id"]
    else:
        return "❌ Bus not found"

    # 🔥 INSERT REASON
    data = {
        "bus_log_id": bus_log_id,
        "reason_text": reason
    }

    r = requests.post(REASON_URL, headers=headers, json=data)

    print("Reason Saved:", r.status_code)

    return "✅ Reason submitted successfully!"


# 🔥 RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)