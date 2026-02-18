# 🌫️ AtmosAI: Real-Time AQI Monitoring & Prediction System

**AtmosAI** is a full-stack web application that lets users **monitor real-time Air Quality Index (AQI) for any city** and get a **next-hour AQI prediction** using a lightweight AI model. The project demonstrates **API integration, data visualization, and basic machine learning** in an interactive dashboard.

---
## Air Quality Index (AQI) Guide

The **Air Quality Index (AQI)** shows how clean or polluted the air is and its health effects.

| AQI Range | Category                        | Health Implications                                                                 |
|-----------|---------------------------------|-----------------------------------------------------------------------------------|
| 0 – 50    | Good                            | Air quality is satisfactory; little or no health risk                               |
| 51 – 100  | Moderate / Satisfactory         | Acceptable; sensitive individuals may be slightly affected                         |
| 101 – 200 | Unhealthy for Sensitive Groups  | Sensitive people may experience health effects; general public usually fine        |
| 201 – 300 | Unhealthy                       | Everyone may begin to experience adverse health effects; sensitive groups more affected |

## Features
-  **Real-time AQI:** Fetches current AQI from [WAQI API](https://aqicn.org/api/).  
-  **Next-hour AQI Prediction:** Uses a simple linear regression model trained on recent AQI trends.  
-  **Graphical Visualization:** Displays current and predicted AQI in an interactive line chart.  
-  **Full-stack Implementation:**  
  - Backend: **Python + Flask**  
  - Frontend: **React + Vite + Chart.js**  
-  **Secure API Key:** Stored in `.env` file, never exposed in code.

---

## Tech Stack
- **Python** – Backend logic & linear regression model  
- **Flask** – REST API server  
- **React + Vite** – Frontend dashboard  
- **Chart.js** – AQI trend visualization  
- **WAQI API** – Real-time air quality data  
- **python-dotenv** – Environment variable management

---

## Getting Started

### Backend
1. Clone the repo:
```bash
git clone https://github.com/yashdeep7733/AtmosAI-Real-Time-AQI-Monitoring-Prediction-System.git
cd AtmosAI/backend
```
2.	Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows
```
3.	Install dependencies:
```bash
pip install -r requirements.txt
```
4.	Add your WAQI API key in .env:
```bash
API_KEY=your_api_key_here
```
5.	Run the backend server:
```bash
python app.py
```
### Frontend
1.	Navigate to frontend folder:
```bash
cd ../frontend
```
2.	Install dependencies and run:
```bash
npm install
npm run dev
```
3.	Open in browser (usually at http://localhost:5173) and enter a city to check AQI.

## Future Improvements
- Train with **real historical AQI data** for more accurate predictions.  
- Predict **multi-hour or daily AQI trends**.  
- Include **weather and pollution features** for smarter predictions.  
- Deploy on **Vercel, Render, or Heroku** for public access.
