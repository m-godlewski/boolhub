import axios from "axios";

const AirService = {
  // url of central backend
  url: "http://localhost/api/",

  getRooms: function () {
    // fetches list of rooms from backend
    return axios.get(this.url + "rooms/").then((response) => response.data);
  },
};

export default AirService;
