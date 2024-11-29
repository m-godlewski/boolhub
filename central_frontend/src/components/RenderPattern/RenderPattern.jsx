import Air from "./Air.jsx";
import Monitoring from "./Monitoring.jsx";
import Cleaning from "./Cleaning.jsx";
import Plants from "./Plants.jsx";
import Settings from "./Settings/Settings.jsx";

export default function RenderPattern({ selectedButton }) {
  switch (selectedButton) {
    case "air":
      return (
        <div id="render-pattern">
          <Air />
        </div>
      );
    case "monitoring":
      return (
        <div id="render-pattern">
          <Monitoring />
        </div>
      );
    case "cleaning":
      return (
        <div id="render-pattern">
          <Cleaning />
        </div>
      );
    case "plants":
      return (
        <div id="render-pattern">
          <Plants />
        </div>
      );
    case "settings":
      return (
        <div id="render-pattern">
          <Settings />
        </div>
      );
  }
}
