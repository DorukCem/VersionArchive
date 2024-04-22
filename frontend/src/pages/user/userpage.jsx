import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./user.css";
import NewRepo from "../newrepo/NewRepo";
import Protected from "../../components/protected/protected";

const navLinkStyle = {
  textDecoration: "none",
  fontSize: "1.3rem",
  fontWeight: 600,
  color: "#fff",
};

export default function UserProfile() {
  const [repos, setRepos] = useState([]);
  const [userNotFound, setUserNotFound] = useState(false);
  const { username } = useParams();
  const [buttonPressed, setButtonPressed] = useState(false);
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    async function fetchUserRepos() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/repo/${username}/all-repos`
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
  }, [username, refresh]);

  const handleCreateRepo = () => {
    setButtonPressed(true);
  };

  const refreshRepos = () => {
    setRefresh(refresh + 1);
  };

  if (userNotFound) {
    return <div>User not found</div>;
  }

  if (buttonPressed) {
    return (
      <NewRepo
        setButtonPressed={setButtonPressed}
        username={username}
        refreshRepos={refreshRepos}
      ></NewRepo>
    );
  }

  return (
    <div>
      <h1>{username}'s Repositories</h1>
      <Protected>
        <button onClick={handleCreateRepo}>Create a new Repository</button>
      </Protected>
      <div className="container">
        <ul>
          {repos.map((reponame, id) => (
            <li className="list-item" key={id}>
              <NavLink style={navLinkStyle} to={`${reponame}`}>
                {reponame}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
