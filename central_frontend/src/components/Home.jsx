import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import { AppProvider } from "@toolpad/core/AppProvider";
import { DashboardLayout } from "@toolpad/core/DashboardLayout";
import { useDemoRouter } from "@toolpad/core/internal";
// icons
import DashboardIcon from "@mui/icons-material/Dashboard";
import AirIcon from "@mui/icons-material/Air";
import VideocamIcon from "@mui/icons-material/Videocam";
import SettingsIcon from "@mui/icons-material/Settings";
import NotificationsIcon from "@mui/icons-material/Notifications";
import DevicesOtherIcon from "@mui/icons-material/DevicesOther";
import ApiIcon from "@mui/icons-material/Api";
import SettingsSystemDaydreamIcon from "@mui/icons-material/SettingsSystemDaydream";
// components
import Dashboard from "./Dashboard.jsx";
import Air from "./Air.jsx";
import Monitoring from "./Monitoring.jsx";
import SettingsNotifications from "./Settings/SettingsNotifications.jsx";
import SettingsDevices from "./Settings/SettingsDevices.jsx";
import SettingsAPI from "./Settings/SettingsAPI.jsx";
import SettingsSystem from "./Settings/SettingsSystem.jsx";

// navigation menu structure
const NAVIGATION = [
  {
    segment: "dashboard",
    title: "Strona Główna",
    icon: <DashboardIcon />,
  },
  {
    segment: "air",
    title: "Powietrze",
    icon: <AirIcon />,
  },
  {
    segment: "monitoring",
    title: "Monitoring",
    icon: <VideocamIcon />,
  },
  {
    kind: "divider",
  },
  {
    segment: "settings",
    title: "Ustawienia",
    icon: <SettingsIcon />,
    children: [
      {
        segment: "notifications",
        title: "Powiadomienia",
        icon: <NotificationsIcon />,
      },
      {
        segment: "devices",
        title: "Urządzenia",
        icon: <DevicesOtherIcon />,
      },
      {
        segment: "api",
        title: "API",
        icon: <ApiIcon />,
      },
      {
        segment: "system",
        title: "System",
        icon: <SettingsSystemDaydreamIcon />,
      },
    ],
  },
];

// function handling page content
function PageContent({ pathname }) {
  // content to render
  let content = <Dashboard />;
  // switch statement that controls page content
  switch (pathname) {
    case "/air":
      return (content = <Air />);
    case "/monitoring":
      return (content = <Monitoring />);
    case "/settings/notifications":
      return (content = <SettingsNotifications />);
    case "/settings/devices":
      return (content = <SettingsDevices />);
    case "/settings/api":
      return (content = <SettingsAPI />);
    case "/settings/system":
      return (content = <SettingsSystem />);
  }
  // returns page content
  return (
    <Box
      sx={{
        py: 4,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        textAlign: "center",
      }}
    >
      {content}
    </Box>
  );
}

PageContent.propTypes = {
  pathname: PropTypes.string.isRequired,
};

function HomePageLayout() {
  // page view router
  const router = useDemoRouter("/dashboard");

  return (
    <AppProvider
      navigation={NAVIGATION}
      branding={{
        logo: <img src="./favicon.ico" />,
        title: "BoolHub",
        homeUrl: "/dashboard",
      }}
      router={router}
    >
      <DashboardLayout>
        <PageContent pathname={router.pathname} />
      </DashboardLayout>
    </AppProvider>
  );
}

HomePageLayout.propTypes = { window: PropTypes.func };

export default HomePageLayout;
