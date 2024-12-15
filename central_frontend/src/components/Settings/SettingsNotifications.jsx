import { useEffect, useState } from "react";
import { getSettings, putSettings } from "./Service";
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
import SaveAltOutlinedIcon from "@mui/icons-material/SaveAltOutlined";

export default function SettingsNotifications() {
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

  // method that handle form submitting
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
    <Box
      sx={{
        padding: "2em",
        "& > :not(style)": { m: 1 },
      }}
    >
      <form onSubmit={handleSubmit}>
        <Fab
          variant="extended"
          type="submit"
          color="primary"
          sx={{ bottom: "3em", right: "3em", position: "fixed" }}
        >
          Zapisz
          <SaveAltOutlinedIcon sx={{ m: 1 }} />
        </Fab>
        {/* air */}
        <Accordion>
          <AccordionSummary
            expandIcon={<KeyboardArrowDownIcon sx={{ color: "white" }} />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography sx={{ fontWeight: "bold" }}>Powietrze</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack orientation="column" spacing={3}>
              {/* air - temperature */}
              <Stack direction="row" spacing={2}>
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
                  <FormHelperText>Powiadomienia o temperaturze</FormHelperText>
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
              <Stack direction="row" spacing={2}>
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
                  <FormHelperText>Powiadomienia o wilgotności</FormHelperText>
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
              <Stack direction="row" spacing={2}>
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
                  <FormHelperText>
                    Powiadomienia o zanieczyszczeniu
                  </FormHelperText>
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
          <AccordionSummary
            expandIcon={<KeyboardArrowDownIcon sx={{ color: "white" }} />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography sx={{ fontWeight: "bold" }}>Diagnostyka</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack direction="row" spacing={2}>
              <FormControl>
                <FormHelperText>Minimalny poziom baterii</FormHelperText>
                <TextField
                  type="number"
                  name="health_threshold"
                  required
                  value={settings.health_threshold}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Powiadomienia diagnostyczne</FormHelperText>
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
          <AccordionSummary
            expandIcon={<KeyboardArrowDownIcon sx={{ color: "white" }} />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography sx={{ fontWeight: "bold" }}>Sieć</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack direction="row" spacing={2}>
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
