import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./user.css";
import NewRepo from "../../components/newrepo/NewRepo";
import Protected from "../../components/protected/protected";
import useAuth from "../../hooks/useAuth";


export default function UserProfile() {
  const [repos, setRepos] = useState([]);
  const [userNotFound, setUserNotFound] = useState(false);
  const { username } = useParams();
  const [buttonPressed, setButtonPressed] = useState(false);
  const [refresh, setRefresh] = useState(0);

  const navigate = useNavigate()

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

  const { auth } = useAuth();

  return (
    <div className="page-container">
      <div className="user-container">
        <div className="header">
          <h1 className="title">
            {auth?.username ? "My Repositories" : `User ${username}'s Repositories`}
          </h1>
          <div className="button-container">
            <Protected>
              <button className="create-repo-button" onClick={handleCreateRepo}>
                Create New
              </button>
            </Protected>
          </div>
        </div>
        <div className="list-container">
          <ul className="list">
            {repos.map((reponame, id) => (
              <li className="list-item" key={id} onClick={() => navigate(`${reponame}`)}>
                  <i className="bi bi-folder-fill"></i>
                  <span className="li-text">{reponame}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
