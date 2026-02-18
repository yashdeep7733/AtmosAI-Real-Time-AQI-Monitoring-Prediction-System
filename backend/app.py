from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pickle
import numpy as np
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load model
model_data = pickle.load(open("aqi_model.pkl", "rb"))

# Ensuring that w and b are scalars values, not arrays
w = float(np.array(model_data["w"]).flatten()[0])
b = float(np.array(model_data["b"]).flatten()[0])

load_dotenv()  # loading stuff from .env

API_KEY = os.getenv("API_KEY") # your WAQI API key from .env


@app.route("/aqi")
def get_aqi():
    city = request.args.get("city")

    try:
        url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}" # AQI API endpoint
        response = requests.get(url, timeout=5) # Add timeout to prevent hanging
        data = response.json() # Convert response to JSON

        if data["status"] != "ok": # Check if API response is successful
            raise Exception("Invalid city") # Handle invalid city or API errors

        current_aqi = data["data"]["aqi"] # Extract current AQI value

    except Exception:
        return jsonify({
            "city": city,
            "current_aqi": None,
            "predicted_aqi": None,
            "error": "Failed to fetch AQI data"
        })

    # Simple linear regression prediction (scalar math)
    predicted_change = w * current_aqi + b

    # Limit unrealistic change predictions to a reasonable range (e.g., -30 to +30)
    predicted_change = max(min(predicted_change, 30), -30) 

    predicted_aqi = current_aqi + predicted_change

    return jsonify({
        "city": city,
        "current_aqi": current_aqi,
        "predicted_aqi": predicted_aqi,
        "error": None
    })

if __name__ == "__main__":
    app.run(debug=True)