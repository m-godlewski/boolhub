import { useState } from "react";
import { Button, Switch, TextField, FormHelperText } from "@mui/material";
import { putSettings } from "./SettingsService";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid2";

// panel of selected tab
function TabPanel(props) {
  // panel properties
  const { children, value, index, ...other } = props;
  // returns panel in form of div
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={"simple-tabpanel-${index}"}
      aria-labelledby={"simple-tab-${index}"}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

// returns tab properties
function tabProps(index) {
  return {
    id: "simple-tab-${index}",
    "aria-controls": "simple-tabpanel-${index}",
  };
}

export default function SettingsForm({ settings, setSettings }) {
  // method that handle submit button click
  const handleSubmit = (e) => {
    e.preventDefault();
    putSettings(e.target.getElementsByTagName("input")).then(
      (result) => {
        alert(result);
      },
      (error) => {
        alert(error);
      }
    );
  };

  // method that handle modifying of input fields
  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  // method that handle modifying of input fields
  const handleClick = (e) => {
    const { name, checked } = e.target;
    setSettings((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  // state of selected tab
  const [selectedTab, setSelectedTab] = useState(0);
  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  return (
    // form
    <form onSubmit={handleSubmit}>
      <Box
        sx={{
          minHeight: "68vh",
          ".MuiFormHelperText-root": {
            color: "white",
            fontWeight: "bold",
            paddingTop: "10%",
            paddingBottom: "2%",
          },
          ".MuiOutlinedInput-input": { color: "white", size: "small" },
          ".Mui-selected": { fontWeight: "bold", color: "#1976d2" },
        }}
      >
        <Box>
          <Tabs
            variant="fullWidth"
            value={selectedTab}
            onChange={handleTabChange}
            textColor="inherit"
          >
            <Tab label="Powietrze" {...tabProps(0)} />
            <Tab label="Urządzenia" {...tabProps(1)} />
            <Tab label="Pogoda" {...tabProps(2)} />
          </Tabs>
        </Box>
        {/* air */}
        <TabPanel value={selectedTab} index={0}>
          <Grid container spacing={10}>
            <Grid size={4}>
              <FormHelperText>Minimalna temperatura</FormHelperText>
              <TextField
                type="number"
                name="temperature_min"
                required
                value={settings.temperature_min}
                onChange={handleChange}
              />
              <FormHelperText>Maksymalna temperatura</FormHelperText>
              <TextField
                type="number"
                name="temperature_max"
                required
                value={settings.temperature_max}
                onChange={handleChange}
              />
              <FormHelperText>Powiadomienia o temperaturze</FormHelperText>
              <Switch
                name="notify_temperature"
                value={settings.notify_temperature ? true : false}
                checked={settings.notify_temperature ? true : false}
                onClick={handleClick}
              />
            </Grid>
            <Grid size={4}>
              <FormHelperText>Minimalna wilgotność</FormHelperText>
              <TextField
                type="number"
                name="humidity_min"
                required
                value={settings.humidity_min}
                onChange={handleChange}
              />
              <FormHelperText>Maksymalna wilgotność</FormHelperText>
              <TextField
                type="number"
                name="humidity_max"
                required
                value={settings.humidity_max}
                onChange={handleChange}
              />
              <FormHelperText>Powiadomienia o wiglnotności</FormHelperText>
              <Switch
                name="notify_humidity"
                value={settings.notify_humidity ? true : false}
                checked={settings.notify_humidity ? true : false}
                onClick={handleClick}
              />
            </Grid>
            <Grid size={4}>
              <FormHelperText>Próg zanieczyszczenia</FormHelperText>
              <TextField
                type="number"
                name="aqi_threshold"
                required
                value={settings.aqi_threshold}
                onChange={handleChange}
              />
              <FormHelperText>Powiadomienia o zanieczyszczeniu</FormHelperText>
              <Switch
                name="notify_aqi"
                value={settings.notify_aqi ? true : false}
                checked={settings.notify_aqi ? true : false}
                onClick={handleClick}
              />
            </Grid>
          </Grid>
        </TabPanel>
        {/* devices */}
        <TabPanel value={selectedTab} index={1}>
          <Grid container spacing={10}>
            <Grid size={6}>
              <FormHelperText>Próg obciążenia sieci</FormHelperText>
              <TextField
                type="number"
                name="network_overload_threshold"
                required
                value={settings.network_overload_threshold}
                onChange={handleChange}
              />
              <FormHelperText>Powiadamiaj o obciążeniu sieci</FormHelperText>
              <Switch
                name="notify_network_overload"
                value={settings.notify_network_overload ? true : false}
                checked={settings.notify_network_overload ? true : false}
                onClick={handleClick}
              />
              <FormHelperText>
                Powiadamiaj o nieznanym urządzeniu w sieci
              </FormHelperText>
              <Switch
                name="notify_unknown_device"
                value={settings.notify_unknown_device ? true : false}
                checked={settings.notify_unknown_device ? true : false}
                onClick={handleClick}
              />
            </Grid>
            <Grid size={6}>
              <FormHelperText>Poziom baterii/filtra</FormHelperText>
              <TextField
                type="number"
                name="health_threshold"
                required
                value={settings.health_threshold}
                onChange={handleChange}
              />
              <FormHelperText>Powiadomienia diagnostyczne</FormHelperText>
              <Switch
                name="notify_health"
                value={settings.notify_health ? true : false}
                checked={settings.notify_health ? true : false}
                onClick={handleClick}
              />
            </Grid>
          </Grid>
        </TabPanel>
        {/* weather */}
        <TabPanel value={selectedTab} index={2}>
          <Grid container spacing={10}>
            <Grid size={6}>
              <FormHelperText>API systemu pogodowego</FormHelperText>
              <TextField
                type="text"
                name="weather_api_url"
                value={settings.weather_api_url}
                onChange={handleChange}
              />
              <FormHelperText>Szerokość Geograficzna</FormHelperText>
              <TextField
                type="text"
                name="weather_api_latitude"
                value={settings.weather_api_latitude}
                onChange={handleChange}
              />
            </Grid>

            <Grid size={6}>
              <FormHelperText>API Token</FormHelperText>
              <TextField
                type="text"
                name="weather_api_token"
                value={settings.weather_api_token}
                onChange={handleChange}
              />
              <FormHelperText>Długość Geograficzna</FormHelperText>
              <TextField
                type="text"
                name="weather_api_longitude"
                value={settings.weather_api_longitude}
                onChange={handleChange}
              />
            </Grid>
          </Grid>
        </TabPanel>
      </Box>
      <Button variant="contained" type="submit">
        Zapisz
      </Button>
    </form>
  );
}
