import Card from "@mui/material/Card";
import Typography from "@mui/material/Typography";
import { Stack } from "@mui/material";

export default function AirRoomCard({ roomName }) {
  const dataTypes = ["Temperatura", "Wilgnotność", "Zanieczyszczenie"];
  return (
    <Card sx={{ p: "5%" }}>
      <Typography variant="h5" sx={{ p: "0 0 3vh 0" }}>
        {roomName}
      </Typography>
      <Stack direction="row" spacing={2}>
        {dataTypes.map((type) => (
          <p>{type}</p>
        ))}
      </Stack>
    </Card>
  );
}
