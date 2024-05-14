import React, { useState } from "react";
import axios from "axios";
import { NavLink } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import "./loginpage.css";

function Login() {
  const { setAuth } = useAuth();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();

    try {
      var bodyFormData = new FormData();
      for (var key in formData) {
        bodyFormData.append(key, formData[key]);
      }

      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/token",
        data: bodyFormData,
        headers: { "Content-Type": "multipart/form-data" },
      });

      const access_token = response?.data?.access_token;
      const username = formData.username;
      setAuth({ username, access_token });
    } catch (error) {
      if (error.response && error.response.status === 401) {
        // Password is wrong
        setError("Password or username is wrong");
      } else {
        // Handle other errors
        console.error(error);
      }
    }
  };

  const onLogout = () => {
    // Clear the authentication state
    setAuth({});
  };

  const { auth } = useAuth();
  if (auth?.username) {
    return (
      <div>
        <h1>User {auth.username} logged in</h1>
        <button onClick={onLogout}>Logout</button>
      </div>
    );
  }

  return (
    <div classname="login-container">
      <form onSubmit={onSubmit} className="form">
        <input
          className="login-input"
          type="text"
          onChange={(e) =>
            setFormData({ ...formData, username: e.target.value })
          }
          placeholder="Username"
          value={formData.username}
        />
        <input
          type="password"
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          placeholder="Password"
          value={formData.password}
        />
        <button type="submit">login</button>
        <p className="message">
          Don't have an account? <NavLink to="/signup">Sign Up</NavLink>
        </p>
      </form>
      {error && <p className="error" style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Login;
