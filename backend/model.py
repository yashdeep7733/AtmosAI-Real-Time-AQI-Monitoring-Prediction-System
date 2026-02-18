import requests
import pickle
import numpy as np
import os

API_KEY = os.getenv("API_KEY") # your WAQI API key from .env
CITY = "jaipur"  # change if you want another city

# Fetch current AQI from WAQI API
url = f"https://api.waqi.info/feed/{CITY}/?token={API_KEY}"
response = requests.get(url)
data = response.json()

if data["status"] != "ok":
    raise Exception("Failed to fetch AQI data")

current_aqi = data["data"]["aqi"]

# Simulate last 24-hour AQI trend around current AQI
np.random.seed(42)
X = np.array([current_aqi + np.random.randint(-10, 10) for _ in range(24)])
y = X[1:] - X[:-1]  # actual next-hour change

# Train linear regression model (simple gradient descent)
X_train = X[:-1]
w = 0
b = 0
lr = 0.0001
epochs = 1000
n = len(X_train)

for _ in range(epochs):
    y_pred = w * X_train + b
    dw = (-2 / n) * np.sum(X_train * (y - y_pred))
    db = (-2 / n) * np.sum(y - y_pred)
    w -= lr * dw
    b -= lr * db

# Save model for app.py
pickle.dump({"w": w, "b": b}, open("aqi_model.pkl", "wb"))

if __name__ == "__main__":
    print("Model trained using recent AQI trend")
    print("Current AQI:", current_aqi)
    print("w:", w, "b:", b)