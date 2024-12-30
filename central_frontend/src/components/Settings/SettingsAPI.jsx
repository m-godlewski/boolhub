// react
import { useEffect, useState } from "react";
// service
import SettingsService from "./Service.jsx";
// material ui
import { TextField, FormHelperText, FormControl } from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Box from "@mui/material/Box";
import Fab from "@mui/material/Fab";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
// icons
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import SaveAltOutlinedIcon from "@mui/icons-material/SaveAltOutlined";

export default function SettingsAPI() {
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
    SeSettingsServicervice.update(e.target.getElementsByTagName("input")).then(
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
        {/* Weather API */}
        <Accordion>
          <AccordionSummary
            expandIcon={<KeyboardArrowDownIcon sx={{ color: "white" }} />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography sx={{ fontWeight: "bold" }}>Weather API</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack direction="row" spacing={2}>
              <FormControl>
                <FormHelperText>API URL</FormHelperText>
                <TextField
                  type="text"
                  name="weather_api_url"
                  value={settings.weather_api_url}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>API Token</FormHelperText>
                <TextField
                  type="text"
                  name="weather_api_token"
                  value={settings.weather_api_token}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Szerokość Geograficzna</FormHelperText>
                <TextField
                  type="text"
                  name="weather_api_latitude"
                  value={settings.weather_api_latitude}
                  onChange={handleChange}
                />
              </FormControl>
              <FormControl>
                <FormHelperText>Długość Geograficzna</FormHelperText>
                <TextField
                  type="text"
                  name="weather_api_longitude"
                  value={settings.weather_api_longitude}
                  onChange={handleChange}
                />
              </FormControl>
            </Stack>
          </AccordionDetails>
        </Accordion>
        {/* NTFY API */}
        <Accordion>
          <AccordionSummary
            expandIcon={<KeyboardArrowDownIcon sx={{ color: "white" }} />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography sx={{ fontWeight: "bold" }}>NTFY API</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Stack direction="row" spacing={2}>
              <FormControl>
                <FormHelperText>NTFY token</FormHelperText>
                <TextField
                  type="text"
                  name="ntfy_token"
                  value={settings.ntfy_token}
                  onChange={handleChange}
                />
              </FormControl>
            </Stack>
          </AccordionDetails>
        </Accordion>
      </form>
    </Box>
  );
}
