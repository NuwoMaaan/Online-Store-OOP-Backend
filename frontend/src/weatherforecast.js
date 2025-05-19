import React, { useEffect, useState } from "react";

function Weather() {
  const [forecast, setForecast] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5203/weatherforecast") // relace with actual API URL
      .then((response) => response.json())
      .then((data) => setForecast(data))
      .catch((err) => console.error("Error fetching forecast:", err));
  }, []);

  return (
    <div>
      <h2>Weather Forecast</h2>
      <ul>
        {forecast.map((item, idx) => (
          <li key={idx}>
            {item.date} - {item.temperatureC}°C - {item.summary}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Weather;
