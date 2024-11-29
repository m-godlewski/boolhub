import { useEffect, useState } from "react";
import SettingsForm from "./SettingsForm";
import axios from "axios";


function getSettings() {
  // fetches current settings from backend
  return axios.get("http://localhost:8080/api/settings")
    .then(response => response.data)
}

export function putSettings(settings) {
  // send updated settings to backend
  return axios.put("http://localhost:8080/api/settings/", {
    "temperature_min": settings.temperature_min.value,
    "temperature_max": settings.temperature_max.value,
    "humidity_min": settings.humidity_min.value,
    "humidity_max": settings.humidity_max.value,
    "aqi_threshold": settings.aqi_threshold.value,
    "network_overload_threshold": settings.network_overload_threshold.value,
    "health_threshold": settings.health_threshold.value,
    "weather_api_url": settings.weather_api_url.value,
    "weather_api_latitude": settings.weather_api_latitude.value,
    "weather_api_longitude": settings.weather_api_longitude.value,
    "weather_api_token": settings.weather_api_token.value
  })
    .then(response => response.data)
}


export default function Settings() {

  // current settings state
  const [settings, setSettings] = useState([]);

  // fetching current settings from backend API
  useEffect(() => {
    let mounted = true;
    getSettings()
      .then(data => {
        if (mounted) {
          setSettings(data)
        }
      })
    return () => mounted = false;
  }, [])


  // renders settings form
  return (
    <div>
      <h1>Settings</h1>
      <SettingsForm settings={settings}/>
    </div>
  );
};
