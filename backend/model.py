import requests
import numpy as np


def safe_float(value):
    try:
        if value is None:
            return None
        if value == "-" or value == "":
            return None
        return float(value)
    except:
        return None


def train_and_predict(city, api_key):
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data.get("status") != "ok":
        raise Exception("Invalid city or API error")

    current_aqi = safe_float(data["data"].get("aqi"))

    if current_aqi is None:
        raise Exception("AQI data not available for the specified city")

    history = []
    forecast = data["data"].get("forecast", {}).get("daily", {}).get("pm25", [])

    for day in forecast:
        value = safe_float(day.get("avg"))
        if value is not None:
            history.append(value)

    # If not enough data, return current only
    if len(history) < 2:
        return current_aqi, current_aqi, history

    # Linear Regression
    y = np.array(history, dtype=float)
    X = np.arange(len(y))

    # y = wx + b
    w, b = np.polyfit(X, y, 1)

    next_time = len(y)
    predicted_aqi = float(w * next_time + b)

    # Clamp unrealistic jumps
    if abs(predicted_aqi - current_aqi) > 40:
        predicted_aqi = current_aqi + np.sign(predicted_aqi - current_aqi) * 40

    return float(current_aqi), float(predicted_aqi), history