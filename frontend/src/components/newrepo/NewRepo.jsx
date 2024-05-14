import { useState } from "react";
import axios from "axios";
import "./newrepopage.css";

export default function NewRepo({ setButtonPressed, username, refreshRepos }) {
  const [repoName, setRepoName] = useState('');
  const [error, setError] = useState("");

  const url = `http://127.0.0.1:8000/repo/${username}/create/${repoName}`
  const handleSubmitRepo = () => {
    axios.post(url, {
      // Add any data you want to send in the request body
    })
      .then(response => {
        console.log('Response:', response.data);
        // Handle the response data
        refreshRepos()
        setButtonPressed(false);
      })
      .catch(error => {
        if (error.response) {
          // The request was made and the server responded with a status code
          console.log('Server responded with an error status:', error.response.status);
          console.log('Response data:', error.response.data);
          setError(error.response.data.detail)
        } else if (error.request) {
          // The request was made but no response was received
          console.error('No response received:', error.request);
          setError("Server is down")
        } else {
          // Something happened in setting up the request that triggered an error
          console.error('Error setting up the request:', error.message);
          setError("Bad request")
        }
        // Handle other types of errors
      });

  };

  const handleCancel = () => {
    setButtonPressed(false);
  };

  return (  
    <div className="container">
      <p>Enter a name for you Repository</p>
      <input className="input-bar"
        type="text"
        placeholder="Repository-Name"
        value={repoName}
        onChange={(e) => setRepoName(e.target.value)}
      />
      <div className="button-container">
        <button className="but" onClick={handleSubmitRepo}>Submit</button>
        <button className="but" onClick={handleCancel}>Cancel</button>
      </div>
      <p>{error}</p>
    </div>
  );
}
