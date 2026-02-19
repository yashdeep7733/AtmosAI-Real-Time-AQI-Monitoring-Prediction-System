import React, { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler);

export default function App() {
  const [city, setCity] = useState("");
  const [aqiData, setAqiData] = useState(null);
  const [loading, setLoading] = useState(false);

  const getAQIAlert = (aqi) => {
    if (aqi <= 50) return "Good : Air is healthy.";
    if (aqi <= 140) return "Decent : Air quality is okay enough.";
    if (aqi <= 160) return "Moderate : Air is okay, sensitive people be cautious.";
    if (aqi <= 200) return "Unhealthy : Limit outdoor activity.";
    if (aqi <= 250) return "Very Unhealthy : Avoid outdoor activity, wear a mask if necessary.";
    return "Hazardous : Stay indoors.";
  };

  const fetchAQI = () => {
    if (!city) return;

    setLoading(true);
    setAqiData(null);

    axios
      .get(`http://127.0.0.1:5000/aqi?city=${city}`)
      .then((res) => setAqiData(res.data))
      .catch(() =>
        setAqiData({ error: "Server not reachable", current_aqi: null })
      )
      .finally(() => setLoading(false));
  };

  const generateSmoothTrend = (current, predicted, steps = 10) => {
    const trend = [];
    for (let i = 0; i <= steps; i++) {
      trend.push(current + ((predicted - current) / steps) * i);
    }
    return trend;
  };

  // Determine Y-axis min and max for better precision
  const getYAxisBounds = (data) => {
    if (!data || data.length === 0) return { min: 0, max: 100 };
    const minVal = Math.min(...data);
    const maxVal = Math.max(...data);
    const padding = (maxVal - minVal) * 0.2 || 5; // 20% padding or at least 5
    return { min: minVal - padding, max: maxVal + padding };
  };

  // Preparing the  chart data
  let trendData = [];
  if (aqiData) {
    if (aqiData.trend) {
      trendData = aqiData.trend;
    } else if (aqiData.current_aqi !== null) {
      trendData = generateSmoothTrend(
        aqiData.current_aqi,
        Number(aqiData.predicted_aqi),
        20
      );
    }
  }

  const chartData = {
    labels: trendData.map((_, i) => i + 1),
    datasets: [
      {
        label: "AQI",
        data: trendData,
        borderColor: "white",
        backgroundColor: "lightblue",
        tension: 0.4,
        fill: false,
      },
    ],
  };

  const yBounds = getYAxisBounds(trendData);

  const chartOptions = {
    scales: {
      y: {
        min: yBounds.min,
        max: yBounds.max,
      },
    },
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>AtmosAI</h1>

      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter city"
      />
      <button onClick={fetchAQI}>Check AQI</button>

      {loading && <div className="shimmer"></div>}

      {aqiData && aqiData.error && (
        <h3 style={{ color: "red" }}>{aqiData.error}</h3>
      )}

      {aqiData && aqiData.current_aqi !== null && (
        <div>
          <h2>City: {aqiData.city}</h2>
          <h3>Current AQI: {aqiData.current_aqi}</h3>
          <h3>Predicted AQI (1hr): {Number(aqiData.predicted_aqi).toFixed(2)}</h3>

          {/* AQI Recommendation */}
          <div style={{ marginTop: "15px", color: "orange", fontWeight: "bold" }}>
            {getAQIAlert(aqiData.current_aqi)}
          </div>

          {/* AQI Chart */}
          <div style={{ width: "400px", margin: "auto", marginTop: "20px" }}>
            <Line data={chartData} options={chartOptions} />
          </div>
        </div>
      )}
    </div>
  );
}