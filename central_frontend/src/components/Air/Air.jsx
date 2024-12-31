// react
import { useEffect, useState } from "react";
// service
import AirService from "./Service.jsx";
// material ui
import Grid from "@mui/material/Grid2";
// components
import AirRoom from "./AirRoom.jsx";

export default function Air() {
  // current rooms state
  const [rooms, setRooms] = useState([]);

  // fetching rooms data from backend
  useEffect(() => {
    let mounted = true;
    AirService.getRoomsAir().then((data) => {
      if (mounted) {
        setRooms(data);
      }
    });
    return () => (mounted = false);
  }, []);

  // renders grid of rooms with air data
  return (
    <Grid
      container
      rowSpacing={1}
      columnSpacing={{ xs: 1, sm: 2, md: 3 }}
      sx={{ width: "100%", p: "3%" }}
    >
      {rooms.map((roomData) => (
        <Grid size={6}>
          <AirRoom roomData={roomData} />
        </Grid>
      ))}
    </Grid>
  );
}
