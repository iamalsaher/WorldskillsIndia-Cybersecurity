import React from "react";
import "./navbar.css";
import { Button } from "antd";
import { useHistory } from "react-router-dom";

const Navbar = ({ reRoute }) => {
  const token = localStorage.getItem("token");
  let history = useHistory();
  console.log(token);
  const logout = () => {
    localStorage.removeItem("token");
    history.push("/login");
  };
  const routeSubmit = () => {
    history.push("/submit");
  };
  return (
    <header>
      <div className="container">
        <div className="logo">
          <span onClick={() => history.push("/")}>
            <h1>Capture The Flag </h1>
          </span>
        </div>

        <input type="checkbox" id="sidebar-toggle" hidden={true} />
        <label htmlFor="sidebar-toggle" className="hamburger">
          <span></span>
        </label>

        <div className="sidebar">
          <nav className="sidebar-nav">
            <ul>
              {token ? (
                <>
                  <li>
                    <Button onClick={routeSubmit}> Submit a flag</Button>
                  </li>
                  <li>
                    <Button onClick={logout}> Logout</Button>
                  </li>
                </>
              ) : (
                <li>
                  <Button onClick={reRoute}> Login</Button>
                </li>
              )}
            </ul>
          </nav>
          <div className="accent"></div>
        </div>
        <div className="sidebar-shadow" id="sidebar-shadow"></div>
        <nav className="desktop-nav">
          <ul>
            {token ? (
              <>
                <li>
                  <Button onClick={routeSubmit}> Submit a flag</Button>
                </li>
                <li>
                  <Button onClick={logout}> Logout</Button>
                </li>
              </>
            ) : (
              <li>
                <Button onClick={reRoute}> Login</Button>
              </li>
            )}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
