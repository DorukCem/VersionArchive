import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function UserProfile() {
  const [repos, setRepos] = useState([]);
  const [userNotFound, setUserNotFound] = useState(false);
  const { username } = useParams();

  useEffect(() => {
    async function fetchUserRepos() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/${username}/all-repos`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setUserNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setRepos(data);
          setUserNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setUserNotFound(true);
      }
    }
    fetchUserRepos();
  }, [username]);

  if (userNotFound) {
    return <div>User not found</div>;
  }

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
