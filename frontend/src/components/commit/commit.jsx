import { useState, useEffect } from "react";
import { useParams, NavLink, useNavigate } from "react-router-dom";
import "./commitpage.css";

export default function Commit({ branchName, commit_id, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [objects, setObjects] = useState([]);
  const [commitInfo, setCommitInfo] = useState(null);
  const navigate = useNavigate();

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
              ID: {commitInfo.oid.substring(0, 10)} | {commitInfo.commit_message} |{" "}
              {commitInfo.timestamp.split("T")[0]}
            </span>
          </div>
          <ul className="commit-list">
            {objects.map((obj) => (
              <li
                className="commit-list-item"
                key={obj.id}
                onClick={() => navigate(`${`object/${obj.oid}`}`)}
              >
                <i class="bi bi-file-earmark"></i>
                <span className="commit-li-text">
                  {obj.name}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : commitInfo !== null ? (
        <h1>This repo is empty, start by commiting a file</h1>
      ) : null}
    </div>
  );
}
