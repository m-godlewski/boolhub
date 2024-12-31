// material ui
import Card from "@mui/material/Card";
import Typography from "@mui/material/Typography";
import { Stack } from "@mui/material";

export default function AirRoom({ roomData }) {
  const translation = {
    aqi: "Zanieczyszczenie",
    temperature: "Temperatura",
    humidity: "Wilgotność",
  };
  return (
    <Card sx={{ p: "5%" }}>
      <Typography variant="h5" sx={{ p: "0 0 5% 0" }}>
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
            <Typography variant="h4" sx={{ textAlign: "center" }}>
              {roomData.airData[k] ? roomData.airData[k] : NaN}
            </Typography>
          </Stack>
        ))}
      </Stack>
    </Card>
  );
}
