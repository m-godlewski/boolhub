import NavigationMenuTile from "./NavigationMenuTile";
import DeviceThermostatTwoToneIcon from "@mui/icons-material/DeviceThermostatTwoTone";
import CameraIndoorTwoToneIcon from "@mui/icons-material/CameraIndoorTwoTone";
import CleaningServicesTwoToneIcon from "@mui/icons-material/CleaningServicesTwoTone";
import LocalFloristTwoToneIcon from "@mui/icons-material/LocalFloristTwoTone";
import SettingsTwoToneIcon from "@mui/icons-material/SettingsTwoTone";

export default function NavigationMenu({ onButtonClick, selectedButton }) {
  return (
    <div id="navigation-menu">
      <NavigationMenuTile
        onClick={() => onButtonClick("air")}
        icon={<DeviceThermostatTwoToneIcon sx={{ fontSize: "6vh" }} />}
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("monitoring")}
        icon={<CameraIndoorTwoToneIcon sx={{ fontSize: "6vh" }} />}
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("cleaning")}
        icon={<CleaningServicesTwoToneIcon sx={{ fontSize: "6vh" }} />}
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("plants")}
        icon={<LocalFloristTwoToneIcon sx={{ fontSize: "6vh" }} />}
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("settings")}
        icon={<SettingsTwoToneIcon sx={{ fontSize: "6vh" }} />}
      />
    </div>
  );
}
