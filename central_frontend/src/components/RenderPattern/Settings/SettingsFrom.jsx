import { useState } from "react";
import {
  Button,
  Switch,
  TextField,
  FormHelperText,
  FormControl,
} from "@mui/material";
import { putSettings } from "./SettingsService";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Grid from "@mui/material/Grid2";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Typography from "@mui/material/Typography";

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
    <form onSubmit={handleSubmit}>
      <Box
        sx={{
          ".MuiFormHelperText-root": {
            color: "white",
            fontWeight: "bold",
            paddingBottom: "0.5em",
          },
          ".MuiOutlinedInput-input": { color: "white", size: "small" },
          ".Mui-selected": { fontWeight: "bold", color: "#1976d2" },
          ".MuiAccordion-root": {
            background: "#252526",
          },
          ".MuiTypography-root": {
            color: "white",
            fontWeight: "bold",
          },
          ".MuiAccordionDetails-root": {
            display: "flex",
            justifyContent: "space-between",
          },
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
            <Tab label="System" {...tabProps(2)} />
          </Tabs>
        </Box>
        {/* air */}
        <TabPanel value={selectedTab} index={0}>
          {/* temperature */}
          <Accordion>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>Temperatura</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <FormHelperText>Minimalna</FormHelperText>
                <TextField
                  type="number"
                  name="temperature_min"
                  required
                  value={settings.temperature_min}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Maksymalna</FormHelperText>
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
            </AccordionDetails>
          </Accordion>
          {/* humidity */}
          <Accordion>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>Wilgotność</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <FormHelperText>Minimum</FormHelperText>
                <TextField
                  type="number"
                  name="humidity_min"
                  required
                  value={settings.humidity_min}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Maksimum</FormHelperText>
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
            </AccordionDetails>
          </Accordion>
          {/* aqi */}
          <Accordion>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>Zanieczyszczenie</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <FormHelperText>Wartość progowa</FormHelperText>
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
            </AccordionDetails>
          </Accordion>
        </TabPanel>
        {/* devices */}
        <TabPanel value={selectedTab} index={1}>
          {/* diagnostics */}
          <Accordion>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>Diagnostyka</Typography>
            </AccordionSummary>
            <AccordionDetails>
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
                <FormHelperText>Powiadomienia</FormHelperText>
                <Switch
                  name="notify_health"
                  value={settings.notify_health ? true : false}
                  checked={settings.notify_health ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
            </AccordionDetails>
          </Accordion>
        </TabPanel>
        {/* system */}
        <TabPanel value={selectedTab} index={2}>
          {/* network */}
          <Accordion>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>Sieć</Typography>
            </AccordionSummary>
            <AccordionDetails>
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
                <FormHelperText>Powiadamiaj o obciążeniu</FormHelperText>
                <Switch
                  name="notify_network_overload"
                  value={settings.notify_network_overload ? true : false}
                  checked={settings.notify_network_overload ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>
                  Powiadamiaj o nieznanym urządzeniu
                </FormHelperText>
                <Switch
                  name="notify_unknown_device"
                  value={settings.notify_unknown_device ? true : false}
                  checked={settings.notify_unknown_device ? true : false}
                  onClick={handleClick}
                />
              </FormControl>
            </AccordionDetails>
          </Accordion>
          {/* weather API */}
          <Accordion sx={{ ".MuiFormControl-root": { width: "100%" } }}>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>API pogodowe</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container rowSpacing={3} columnSpacing={3}>
                <Grid size={6}>
                  <FormControl>
                    <FormHelperText>API URL</FormHelperText>
                    <TextField
                      type="text"
                      name="weather_api_url"
                      value={settings.weather_api_url}
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
                <Grid size={6}>
                  <FormControl>
                    <FormHelperText>API Token</FormHelperText>
                    <TextField
                      type="text"
                      name="weather_api_token"
                      value={settings.weather_api_token}
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
                <Grid size={6}>
                  <FormControl>
                    <FormHelperText>Szerokość Geograficzna</FormHelperText>
                    <TextField
                      type="text"
                      name="weather_api_latitude"
                      value={settings.weather_api_latitude}
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
                <Grid size={6}>
                  <FormControl>
                    <FormHelperText>Długość Geograficzna</FormHelperText>
                    <TextField
                      type="text"
                      name="weather_api_longitude"
                      value={settings.weather_api_longitude}
                      onChange={handleChange}
                    />
                  </FormControl>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
          <Accordion sx={{ ".MuiFormControl-root": { width: "100%" } }}>
            <AccordionSummary
              expandIcon={<KeyboardArrowUpIcon sx={{ color: "white" }} />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              <Typography>API powiadomień</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl>
                <FormHelperText>NTFY token</FormHelperText>
                <TextField
                  type="text"
                  name="ntfy_token"
                  value={settings.ntfy_token}
                  onChange={handleChange}
                />
              </FormControl>
            </AccordionDetails>
          </Accordion>
        </TabPanel>
      </Box>
      <Button variant="contained" type="submit">
        Zapisz
      </Button>
    </form>
  );
}
