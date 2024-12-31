import axios from "axios";

const AirService = {
  // url of central backend
  url: "http://localhost/api/",

  getRoomsAir: function () {
    // fetches list of rooms from backend
    return axios.get(this.url + "rooms/air").then((response) => response.data);
  },
};

export default AirService;
