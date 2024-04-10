import { NavLink } from "react-router-dom";
import "./navbar-styles.css";
import { useState } from "react";

const navLinkStyle = {
  textDecoration: "none",
  fontSize: "1.3rem",
  fontWeight: 600,
  color: "#fff",
};

export default function Navbar() {
  const [menuClicked, setMenuClicked] = useState(false);

  function handleClick() {
    setMenuClicked(!menuClicked);
  }

  return (
    <nav>
      <form>
        <input type="text" name="search" placeholder="Search for User" />
      </form>
      <ul id="navbar" className={menuClicked ? "#navbar active" : "navbar"}>
        <li>
          <NavLink to={"/"} style={navLinkStyle}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to={"/tutorial"} style={navLinkStyle}>
            Tutorial
          </NavLink>
        </li>
      </ul>

      <div id="mobile" onClick={handleClick}>
        <i
          id="bar"
          className={menuClicked ? "fas fa-times" : "fas fa-bars"}
        ></i>
      </div>
    </nav>
  );
}
