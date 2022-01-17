import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Auth from "./pages/auth";
import LeaderBoard from "./pages/leaderBoard";
import SubmitFlag from "./pages/submitFlag";

import "./App.css";

const App = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={(props) => <LeaderBoard {...props} />} />
        <Route exact path="/login" render={(props) => <Auth {...props} />} />
        <Route
          exact
          path="/submit"
          render={(props) => <SubmitFlag {...props} keyx={2} />}
        />
      </Switch>
    </Router>
  );
};

export default App;
