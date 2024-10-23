import { useState } from "react";
import LeftPanel from "./components/LeftPanel";
import RightPanel from "./components/RightPanel";

function App() {
  return (
    <div id="main-panel">
      <LeftPanel />
      <RightPanel />
    </div>
  );
}

export default App;
