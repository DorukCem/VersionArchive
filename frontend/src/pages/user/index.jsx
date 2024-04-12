import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function UserProfile() {
  const [repos, setRepos] = useState([]);
  const { username } = useParams();

  useEffect(() => {
    async function fetchUserRepos() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/${username}/all-repos`
        );
        const data = await response.json();
        setRepos(data);
      } catch (error) {
        console.error("Failed to fetch user repos:", error);
      }
    }
    fetchUserRepos();
  }, [username]);

  return (
    <div className="App">
      <h1>{username}'s Repositories</h1>
      <ul>
        {repos.map((repo, id) => (
          <li key={id}>{repo}</li>
        ))}
      </ul>
    </div>
  );
}
