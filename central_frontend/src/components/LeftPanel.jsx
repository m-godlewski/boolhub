import Clock from "./Clock/Clock";
import Weather from "./Weather/Weather";
import Notifications from "./Notifications/Notifications";
import HouseHolders from "./HouseHolders/HouseHolders";

export default function LeftPanel() {
  return (
    <div id="left-panel">
      <Clock />
      <Weather />
      <Notifications />
      <HouseHolders />
    </div>
  );
}
