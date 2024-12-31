// material ui
import Card from "@mui/material/Card";
import Typography from "@mui/material/Typography";
import { Stack } from "@mui/material";

export default function AirRoom({ roomData }) {
  // translation dictionary
  const translation = {
    aqi: "Zanieczyszczenie",
    temperature: "Temperatura",
    humidity: "Wilgotność",
  };
  // returns proper color base on data type and value
  const checkColor = (type, value) => {
    console.log(value);
    switch (type) {
      case "temperature":
        switch (true) {
          case value === null:
            return "#E0E0E0";
          case value > 28.0:
            return "#FF3333";
          case value > 25.0:
            return "#FF8000";
          case value > 20.0:
            return "#00CC00";
          case value > 15.0:
            return "#00CCCC";
          case value > 0.0:
            return "#0080FF";
          default:
            return "#FFFFFF";
        }
      case "aqi":
        switch (true) {
          case value === null:
            return "#E0E0E0";
          case value > 300:
            return "#660033";
          case value > 200:
            return "#990099";
          case value > 150:
            return "#FF3333";
          case value > 100:
            return "#FF8000";
          case value > 50:
            return "#FFFF00";
          default:
            return "#00CC00";
        }
      case "humidity":
        switch (true) {
          case value === null:
            return "#E0E0E0";
          case value >= 85:
            return "#0080FF";
          case value <= 25:
            return "#FF3333";
          default:
            return "#00CC00";
        }
    }
  };

  return (
    <Card sx={{ p: "2em" }}>
      <Typography
        variant="h5"
        gutterBottom
        sx={{ p: "0 0 1em 0", fontWeight: "bold" }}
      >
        {roomData.name}
      </Typography>
      <Stack
        direction="row"
        sx={{
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        {Object.keys(roomData.airData).map((k) => (
          <Stack>
            <Typography variant="caption">{translation[k]}</Typography>
            <Typography
              variant="h4"
              sx={{
                textAlign: "center",
                color: checkColor(k, roomData.airData[k]),
              }}
            >
              {roomData.airData[k] ? roomData.airData[k] : "?"}
            </Typography>
          </Stack>
        ))}
      </Stack>
    </Card>
  );
}
