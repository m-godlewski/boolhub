import React from "react";
// left panel components
import Clock from "./Clock/Clock";
import Weather from "./Weather/Weather";
import Notifications from "./Notifications/Notifications";
import HouseHolders from "./HouseHolders/HouseHolders";
// right panel components
import RenderPattern from "./RenderPattern/RenderPattern";
import NavigationMenu from "./NavigationMenu/NavigationMenu";

export default function Home() {
  // holding state of displayed pattern
  const [selectedNavigation, setSelectednavigation] = React.useState("air");

  // pattern content
  let content = selectedNavigation;

  // function that handles click of navigation buttons
  function onButtonClick(selectedButton) {
    console.log(selectedButton);
    setSelectednavigation(selectedButton);
  }

  return (
    <div id="main-panel">
      <div id="left-panel">
        <Clock />
        <Weather />
        <Notifications />
        <HouseHolders />
      </div>
      <div id="right-panel">
        <RenderPattern>{content}</RenderPattern>
        <NavigationMenu
          onButtonClick={onButtonClick}
          selectedButton={selectedNavigation}
        />
      </div>
    </div>
  );
}
