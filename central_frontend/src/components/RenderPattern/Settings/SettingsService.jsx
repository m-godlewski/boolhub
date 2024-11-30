import axios from "axios";

export function getSettings() {
  // fetches current settings from backend
  return axios
    .get("http://localhost/api/settings")
    .then((response) => response.data);
}

export function putSettings(settings) {
  // send updated settings to backend
  // object that will store data to update
  let updatedData = {};
  // iterate over fields
  for (let field in settings) {
    // converts number string to integer
    if (settings[field].type === "number") {
      updatedData[settings[field].name] = Number(settings[field].value);
    } else {
      // no conversion
      updatedData[settings[field].name] = settings[field].value;
    }
  }
  return axios
    .put("http://localhost/api/settings/", {
      ...updatedData,
    })
    .then((response) => response.data);
}
