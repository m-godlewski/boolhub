// react
import { useEffect, useState } from "react";
// service
import AirService from "./Service.jsx";
// material ui
import Grid from "@mui/material/Grid2";
// components
import AirRoomCard from "./AirRoomCard.jsx";

export default function Air() {
  // current rooms state
  const [rooms, setRooms] = useState([]);

  // fetching rooms data from backend
  useEffect(() => {
    let mounted = true;
    AirService.getRooms().then((data) => {
      if (mounted) {
        setRooms(data);
      }
    });
    return () => (mounted = false);
  }, []);

  return (
    <Grid
      container
      rowSpacing={1}
      columnSpacing={{ xs: 1, sm: 2, md: 3 }}
      sx={{ width: "100%", p: "3%" }}
    >
      {rooms.map((room) => (
        <Grid size={6}>
          <AirRoomCard roomName={room.name} />
        </Grid>
      ))}
    </Grid>
  );
}
