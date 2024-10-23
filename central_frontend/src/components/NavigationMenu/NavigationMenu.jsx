import NavigationMenuTile from "./NavigationMenuTile";

export default function NavigationMenu({ onButtonClick, selectedButton }) {
  return (
    <div id="navigation-menu">
      <NavigationMenuTile onClick={() => onButtonClick("air")} title="Air" />
      <NavigationMenuTile
        onClick={() => onButtonClick("monitoring")}
        title="Monitoring"
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("network")}
        title="Network"
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("cleaning")}
        title="Cleaning"
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("plants")}
        title="Plants"
      />
      <NavigationMenuTile
        onClick={() => onButtonClick("settings")}
        title="Settings"
      />
    </div>
  );
}
