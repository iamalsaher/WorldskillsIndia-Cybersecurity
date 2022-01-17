import axios from "axios";

const url = "http://159.65.153.16";

// POST - TO login
export const submit = (data, mytoken) => {
  return axios
    .post(url + `/submit`, data, {
      headers: { Authorization: "Bearer " + mytoken },
    })
    .then((response) => {
      console.log("Registered");
      return response.data;
    });
};

// POST - TO submit flags
export const login = (data) => {
  return axios.post(url + `/login`, data, {}).then((response) => {
    console.log("Registered");
    return response.data;
  });
};

// GET - FETCH Leaderboard
export const leaderboard = () => {
  return axios
    .get(url + "/leaderboard", {})
    .then((response) => {
      return response.data;
    })
    .catch((err) => {
      console.log(err);
    });
};
