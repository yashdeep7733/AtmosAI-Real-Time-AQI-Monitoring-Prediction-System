import requests
import numpy as np
import os

def train_and_predict(city, api_key):
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data["status"] != "ok":
        raise Exception("Invalid city or API error")

    current_aqi = data["data"]["aqi"]

    history = []
    forecast = data["data"].get("forecast", {}).get("daily", {}).get("pm25", [])

    for day in forecast:
        history.append(day["avg"])

    if len(history) < 2:
        return current_aqi, current_aqi, history

    # Use historical AQI values
    y = np.array(history)

    # Time index: 0,1,2,...n
    X = np.arange(len(y))

    # Linear regression (least squares)
    w, b = np.polyfit(X, y, 1)

    # Predict next time step
    next_time = len(y)
    predicted_aqi = float(w * next_time + b)

    # Limit unrealistic jumps (safety clamp)
    if abs(predicted_aqi - current_aqi) > 40:
        predicted_aqi = current_aqi + np.sign(predicted_aqi - current_aqi) * 40

    return current_aqi, predicted_aqi, history