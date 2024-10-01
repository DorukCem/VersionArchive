import { useState, useEffect } from "react";
import { useParams, NavLink } from "react-router-dom";
import "./commitpage.css";

export default function Commit({ branchName, commit_id, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [objects, setObjects] = useState([]);
  const [commitInfo, setCommitInfo] = useState(null);
  const navLinkStyle = {
    textDecoration: "none",
    color: "black",
  };

  useEffect(() => {
    async function fetchCommitContents() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/commit/${username}/${repoName}/${branchName}/${commit_id}/objects`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setRepoNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setObjects(data.objects);
          setCommitInfo(data.commit);
          setRepoNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    fetchCommitContents();
  }, [repoName, branchName, commit_id]);

  return (
    <div className="commit-container">
      {objects.length > 0 ? (
        <div>
          <div className="commit-title">
            <span>
              ID: {commit_id} | {commitInfo.commit_message} | {commitInfo.timestamp.split("T")[0]}
            </span>
          </div>
          <ul className="commit-list">
            {objects.map((obj) => (
              <li className="commit-list-item" key={obj.id}>
                <i class="bi bi-file-earmark"></i>
                <span className="commit-li-text">
                  <NavLink style={navLinkStyle} to={`object/${obj.oid}`}>
                    {obj.name}
                  </NavLink>
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <h1>This repo is empty, start by commiting a file</h1>
      )}
    </div>
  );
}
