// react
import { useEffect, useState } from "react";
// service
import SettingsService from "./Service.jsx";
// material ui
import { Switch, TextField, FormHelperText, FormControl } from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Fab from "@mui/material/Fab";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
// icons
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";

export default function SettingsNotifications() {
  // current settings state
  const [settings, setSettings] = useState([]);

  // fetching current settings from backend API
  useEffect(() => {
    let mounted = true;
    SettingsService.get().then((data) => {
      if (mounted) {
        setSettings(data);
      }
    });
    return () => (mounted = false);
  }, []);

  // method that handle form submitting
  const handleSubmit = (e) => {
    e.preventDefault();
    SettingsService.update(e.target.getElementsByTagName("input")).then(
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

  // method that handle modifying of switch fields
  const handleClick = (e) => {
    const { name, checked } = e.target;
    setSettings((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  // renders settings form
  return (
    <Box sx={{ padding: "2em" }}>
      <form onSubmit={handleSubmit}>
        <Fab
          variant="extended"
          type="submit"
          color="primary"
          sx={{ bottom: "3em", right: "3em", position: "fixed" }}
        >
          Zapisz
        </Fab>
        {/* air */}
        <Accordion>
          <AccordionSummary expandIcon={<KeyboardArrowDownIcon />}>
            <Typography gutterBottom sx={{ fontWeight: "bold" }}>
              Powietrze
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack orientation="column" spacing={5}>
              {/* air - temperature */}
              <Stack
                direction="row"
                sx={{
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <FormControl>
                  <FormHelperText>Temperatura minimalna</FormHelperText>
                  <TextField
                    type="number"
                    name="temperature_min"
                    required
                    value={settings.temperature_min}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText>Temperatura maksymalna</FormHelperText>
                  <TextField
                    type="number"
                    name="temperature_max"
                    required
                    value={settings.temperature_max}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText>Powiadomienia</FormHelperText>
                  <Switch
                    name="notify_temperature"
                    value={settings.notify_temperature ? true : false}
                    checked={settings.notify_temperature ? true : false}
                    onClick={handleClick}
                  />
                </FormControl>
              </Stack>

              <Divider />

              {/* air - humidity */}
              <Stack
                direction="row"
                sx={{
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <FormControl>
                  <FormHelperText>Wilgotność minimalna</FormHelperText>
                  <TextField
                    type="number"
                    name="humidity_min"
                    required
                    value={settings.humidity_min}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText>Wilgotność maksymalna</FormHelperText>
                  <TextField
                    type="number"
                    name="humidity_max"
                    required
                    value={settings.humidity_max}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText>Powiadomienia</FormHelperText>
                  <Switch
                    name="notify_humidity"
                    value={settings.notify_humidity ? true : false}
                    checked={settings.notify_humidity ? true : false}
                    onClick={handleClick}
                  />
                </FormControl>
              </Stack>

              <Divider />

              {/* air - aqi */}
              <Stack
                direction="row"
                sx={{
                  justifyContent: "space-between",
                  alignItems: "center",
                  paddingBottom: "1.5em",
                }}
              >
                <FormControl>
                  <FormHelperText>
                    Maksymalna wartość zanieczyszczenia
                  </FormHelperText>
                  <TextField
                    type="number"
                    name="aqi_threshold"
                    required
                    value={settings.aqi_threshold}
                    onChange={handleChange}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText>Powiadomienia</FormHelperText>
                  <Switch
                    name="notify_aqi"
                    value={settings.notify_aqi ? true : false}
                    checked={settings.notify_aqi ? true : false}
                    onClick={handleClick}
                  />
                </FormControl>
              </Stack>
            </Stack>
          </AccordionDetails>
        </Accordion>
        {/* diagnostic */}
        <Accordion>
          <AccordionSummary expandIcon={<KeyboardArrowDownIcon />}>
            <Typography gutterBottom sx={{ fontWeight: "bold" }}>
              Diagnostyka
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack
              direction="row"
              sx={{
                justifyContent: "space-between",
                alignItems: "center",
                paddingBottom: "1.5em",
              }}
            >
              <FormControl>
                <FormHelperText>
                  Minimalny poziom baterii lub filtra
                </FormHelperText>
                <TextField
                  type="number"
                  name="health_threshold"
                  required
                  value={settings.health_threshold}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Powiadomienia</FormHelperText>
                <Switch
                  name="notify_health"
                  value={settings.notify_health ? true : false}
                  checked={settings.notify_health ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
            </Stack>
          </AccordionDetails>
        </Accordion>
        {/* network */}
        <Accordion>
          <AccordionSummary expandIcon={<KeyboardArrowDownIcon />}>
            <Typography gutterBottom sx={{ fontWeight: "bold" }}>
              Sieć
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack
              direction="row"
              sx={{
                justifyContent: "space-between",
                alignItems: "center",
                paddingBottom: "1.5em",
              }}
            >
              <FormControl>
                <FormHelperText>Próg obciążenia sieci</FormHelperText>
                <TextField
                  type="number"
                  name="network_overload_threshold"
                  required
                  value={settings.network_overload_threshold}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Powiadomienia o obciążeniu</FormHelperText>
                <Switch
                  name="notify_network_overload"
                  value={settings.notify_network_overload ? true : false}
                  checked={settings.notify_network_overload ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>
                  Powiadomienia o nieznanym urządzeniu
                </FormHelperText>
                <Switch
                  name="notify_unknown_device"
                  value={settings.notify_unknown_device ? true : false}
                  checked={settings.notify_unknown_device ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
            </Stack>
          </AccordionDetails>
        </Accordion>
      </form>
    </Box>
  );
}
