import React from "react";
import axios from "axios";
import { useState} from "react";
import useAuth from "../../hooks/useAuth";

function Login() {
  const { setAuth } = useAuth();
  const [formData, setFormData] = useState({ username: "", password: "" });

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

      // Handle the response, e.g., store the token in local storage or context
      console.log(response.data.access_token);
      console.log(response.data.token_type);
      const access_token = response?.data?.access_token;
      const username = formData.username
      setAuth({ username, access_token });

    } catch (error) {
      // Handle any errors
      console.log(error);
    }
  };

  const { auth } = useAuth();
  if (auth?.username) {
    return <div>
      <h1>User {auth.username} logged in</h1>
    </div>
  }

  return (
    <form onSubmit={onSubmit}>
      <input
        type="text"
        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
        placeholder="Username"
        value={formData.username}
      />
      <input
        type="password"
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        placeholder="Password"
        value={formData.password}
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default Login;
