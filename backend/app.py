from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from model import train_and_predict

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():
    return jsonify({"status": "AtmosAI backend running"})


@app.route("/aqi", methods=["GET"])
def get_aqi():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    try:
        current_aqi, predicted_aqi, history = train_and_predict(city, API_KEY)

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
            "error": str(e)
        }), 500


@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))