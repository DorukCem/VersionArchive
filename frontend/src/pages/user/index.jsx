import { useState } from "react";

export default function UserProfile({ username }) {
  const [repos, setRepos] = useState([]);

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
        {repos.map((repo) => (
          <li>{repo}</li>
        ))}
      </ul>
    </div>
  );
}
