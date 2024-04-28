import { useState, useEffect } from "react";
import { useParams, NavLink } from "react-router-dom";

export default function Commit({ branchName, commit_oid, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [objects, setObjects] = useState([])


  useEffect(() => {
    async function fetchCommitContents() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/commit/${username}/${repoName}/${branchName}/${commit_oid}/objects`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setRepoNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setObjects(data);
          setRepoNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    fetchCommitContents();
  }, [repoName, branchName, commit_oid]);

  return (
    <div>
      {objects.length > 0 ? (
        <div>
          <h3>
            {repoName} {branchName} commit: {commit_oid} contents
          </h3>
          <ul>
            {objects.map((obj) => (
              <li key={obj.id}>
                <NavLink to={`object/${obj.oid}`}>{obj.name}</NavLink>
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
