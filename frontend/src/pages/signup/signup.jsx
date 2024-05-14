import React, { useState } from "react";
import axios from "axios";
import { NavLink } from "react-router-dom";
import "./signuppage.css";

function SignUp() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/user/create-user",
        formData
      );
      setSuccessMessage("Sign up successful!");
    } catch (error) {
      if (error.response && error.response.status === 409) {
        setError("Username is already taken");
      } else {
        // Handle other errors
        console.log(error);
      }
    }
  };

  if (successMessage !== "") {
    return (
      <div>
        <p style={{ color: "green" }}>{successMessage}</p>
        <p>
          You can now <NavLink to="/login">login</NavLink>
        </p>
      </div>
    );
  }

  return (
    <div className="signup-container">
      <form onSubmit={onSubmit} className="signup-form">
        <h3>Select a username and password</h3>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <input
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
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
