import { useEffect, useState } from "react";
import { getSettings } from "./SettingsService";
import SettingsForm from "./SettingsFrom";

export default function Settings() {
  // current settings state
  const [settings, setSettings] = useState([]);

  // fetching current settings from backend API
  useEffect(() => {
    let mounted = true;
    getSettings().then((data) => {
      if (mounted) {
        setSettings(data);
      }
    });
    return () => (mounted = false);
  }, []);

  // renders settings form
  return (
    <div id="settings-main">
      <h1>Ustawienia</h1>
      <SettingsForm settings={settings} setSettings={setSettings} />
    </div>
  );
}
