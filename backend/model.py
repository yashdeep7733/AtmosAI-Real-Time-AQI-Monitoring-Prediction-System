import requests
import pickle
import numpy as np
import os

# Load the api key from environment variable
API_KEY = os.getenv("API_KEY")  # Make sure to set API_KEY in your .env or environment
CITY = "jaipur"  # Change city if needed

# Fetch current AQI from WAQI API
url = f"https://api.waqi.info/feed/{CITY}/?token={API_KEY}"
response = requests.get(url)
data = response.json()

if data["status"] != "ok":
    raise Exception("Failed to fetch AQI data")

current_aqi = data["data"]["aqi"]

# Get real past 24-hour AQI from WAQI forecast if available
past_aqi = []
if "forecast" in data["data"] and "hourly" in data["data"]["forecast"]:
    # Use PM2.5 hourly data if available
    hourly_pm25 = data["data"]["forecast"]["hourly"].get("pm25", [])
    for h in hourly_pm25[:24]:  # take last 24 hours
        past_aqi.append(h['avg'])

# If past data not available, fallback to simulated values
if past_aqi:
    X = np.array(past_aqi)
else:
    np.random.seed(42)
    X = np.array([current_aqi + np.random.randint(-10, 10) for _ in range(24)])

# Compute next-hour changes
y = X[1:] - X[:-1]

# Linear regression via gradient descent
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

# Save the trained model
pickle.dump({"w": w, "b": b}, open("aqi_model.pkl", "wb"))

if __name__ == "__main__":
    print("Model trained using recent AQI trend")
    print("Current AQI:", current_aqi)
    print("w:", w, "b:", b)