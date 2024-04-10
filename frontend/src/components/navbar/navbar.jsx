import { NavLink } from "react-router-dom";
import "./navbar-styles.css";

const navLinkStyle = {
  textDecoration: 'none',
  fontSize: '1.3rem',
  fontWeight: 600,
  color: '#fff'
};

export default function Navbar() {
  return (
    <nav>
      <form>
        <input type="text" name="search" placeholder="Search for User" />
      </form>
      <ul id="navbar">
        <li>
          <NavLink
            to={"/"}
            style={navLinkStyle}
          >
            Home
          </NavLink>
        </li>
        <li>
          <NavLink
            to={"/tutorial"}
            style={navLinkStyle}
          >
            Tutorial
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}
