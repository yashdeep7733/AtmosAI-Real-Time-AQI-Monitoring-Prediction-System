from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route("/aqi", methods=["GET"])
def get_aqi():
    city = request.args.get("city")

    try:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["status"] != "ok":
            raise Exception("Invalid city")

        current_aqi = data["data"]["aqi"]

        # Extract daily PM2.5 forecast
        history = []
        forecast = data["data"].get("forecast", {}).get("daily", {}).get("pm25", [])

        for item in forecast[:8]:
            history.append(item["avg"])

        # Simple trend prediction
        if len(history) > 1:
            changes = [history[i] - history[i - 1] for i in range(1, len(history))]
            avg_change = sum(changes) / len(changes)
        else:
            avg_change = 0

        predicted_aqi = current_aqi + avg_change

        return jsonify({
            "city": city,
            "current_aqi": current_aqi,
            "predicted_aqi": predicted_aqi,
            "history": history,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "city": city,
            "current_aqi": None,
            "predicted_aqi": None,
            "history": None,
            "error": "Failed to fetch AQI data"
        })
    
# Ping for server up check
@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)