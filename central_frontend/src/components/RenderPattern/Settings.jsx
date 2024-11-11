import { useEffect, useState } from "react";
import axios from "axios";

const FIELDS_TRANSLATION = {
  "PL": {
    "temperature_min": "Minimalna Temperatura",
    "temperature_max": "Maksymalna Temperatura",
    "notify_temperature": "Powiadamiaj o Temperaturze",
    "humidity_min": "Minimalna Wilgotność Powietrza",
    "humidity_max": "Maksymalna Wilgotność Powietrza",
    "notify_humidity": "Powiadamiaj o Wilgotności Powietrza",
    "aqi_threshold": "Próg Zanieczyszczenia Powietrza",
    "notify_aqi": "Powiadamiaj o Zanieczyszczeniu Powietrza",
    "network_overload_threshold": "Próg Obciążenia Sieci",
    "notify_network_overload": "Powiadamiaj o Obciążeniu Sieci",
    "notify_unknown_device": "Powiadamiaj o Nieznanym Urządzeniu w Sieci",
    "health_threshold": "Poziom baterii/filtra",
    "notify_health": "Powiadomienia Diagnostyczne",
    "weather_api_url": "API systemu pogodowego",
    "weather_api_latitude": "Szerokość Geograficzna",
    "weather_api_longitude": "Długość Geograficzna",
  }
}

function getSettings() {
  // fetches current settings from backend
  return axios.get("http://localhost:8080/api/settings")
    .then(response => response.data)
}

function putSettings() {
  // send updated settings to backend
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
      {Object.keys(settings).map(
        function (key) {
          return <p key={key}>{FIELDS_TRANSLATION["PL"][key]} = {settings[key].toString()}</p>
        }
      )}
    </div>
  );
};
