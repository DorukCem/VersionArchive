import { NavLink } from "react-router-dom";
import "./navbar-styles.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const navLinkStyle = {
  textDecoration: "none",
  fontSize: "1.3rem",
  fontWeight: 600,
  color: "#fff",
};

export default function Navbar() {
  const [menuClicked, setMenuClicked] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  function handleClick() {
    setMenuClicked(!menuClicked);
  }

  function handleSearch(e) {
    e.preventDefault();
    if (searchQuery.trim() !== "") {
      navigate(`/${searchQuery}`);
      setSearchQuery("");
    }
  }
  const { auth } = useAuth();

  return (
    <nav>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          name="search"
          placeholder="Search for User"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </form>
      <ul id="navbar" className={menuClicked ? "#navbar active" : "navbar"}>
        <li>
          <NavLink to={"/"} style={navLinkStyle}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to={"/login"} style={navLinkStyle}>
            {auth.username ? "Logout" : "Login"}
          </NavLink>
        </li>
        <li>
          {auth.username && (
            <NavLink to={`/${auth.username}`} style={navLinkStyle}>
              My Repositories
            </NavLink>
          )}
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
