import axios from "axios";

const SettingsService = {
  // url of central backend
  url: "http://localhost/api/",

  get: function () {
    // fetches current settings from backend
    return axios.get(this.url + "settings/").then((response) => response.data);
  },

  update: function (settings) {
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
      .put(this.url + "settings/", {
        ...updatedData,
      })
      .then((response) => response.data);
  },
};

export default SettingsService;
