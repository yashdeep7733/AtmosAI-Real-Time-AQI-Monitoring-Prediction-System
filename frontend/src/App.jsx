import React, { useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function App() {
  // --- States ---
  const [city, setCity] = useState("");
  const [aqiData, setAqiData] = useState(null);
  const [loading, setLoading] = useState(false);

  // --- Fetch AQI ---
  const fetchAQI = () => {
    if (!city) return;

    setLoading(true);
    setAqiData(null);

    axios
      .get(`https://atmosai-8mem.onrender.com/aqi?city=${city}`)
      .then((res) => setAqiData(res.data))
      .catch(() =>
        setAqiData({ error: "Server not reachable", current_aqi: null })
      )
      .finally(() => setLoading(false));
  };

  const chartData = {
    labels: ["Current", "Predicted (1hr)"],
    datasets: [
      {
        label: "AQI",
        data:
          aqiData && aqiData.current_aqi !== null
            ? [aqiData.current_aqi, aqiData.predicted_aqi]
            : [],
        borderColor: "white",
        backgroundColor: "lightblue",
      },
    ],
  };

  // --- Stuff ---
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
          <h3>
            Predicted AQI (1hr): {Number(aqiData.predicted_aqi).toFixed(2)}
          </h3>

          <div style={{ width: "400px", margin: "auto" }}>
            <Line data={chartData} />
          </div>
        </div>
      )}
    </div>
  );
}