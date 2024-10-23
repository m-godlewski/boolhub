import React from "react";
import RenderPattern from "./RenderPattern/RenderPattern";
import NavigationMenu from "./NavigationMenu/NavigationMenu";

export default function RightPanel() {
  //
  const [selectedNavigation, setSelectednavigation] = React.useState("air");

  //
  let content = selectedNavigation;

  //
  function onButtonClick(selectedButton) {
    console.log(selectedButton);
    setSelectednavigation(selectedButton);
  }
  return (
    <div id="right-panel">
      <RenderPattern>{content}</RenderPattern>
      <NavigationMenu
        onButtonClick={onButtonClick}
        selectedButton={selectedNavigation}
      />
    </div>
  );
}
