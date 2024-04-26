import { useState, useEffect } from "react";
import { NavLink, useParams } from "react-router-dom";
import Protected from "../../components/protected/protected";
import NewCommit from "../../components/newcommit/newCommit";

export default function Branch({ branchName, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [objects, setObjects] = useState([]);

  const [buttonPressed, setButtonPressed] = useState(false);
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    async function fetchRepoContents() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/object/${username}/${repoName}/${branchName}/all`
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
    fetchRepoContents();
  }, [repoName, refresh, branchName]);

  const createNewCommit = () => {
    setButtonPressed(true);
  };

  const refreshRepos = () => {
    setRefresh(refresh + 1);
  };

  return (
    <div className="App">
      {objects.length > 0 ? (
        <div>
          <h1>{repoName} {branchName} contents</h1>
          <ul>
            {objects.map((obj) => (
              <li key={obj.id}>
                <NavLink to={`object/${obj.oid}`}>{obj.name}</NavLink>
              </li>
            ))}
          </ul>{" "}
        </div>
      ) : (
        <h1>This repo is empty, start by commiting a file</h1>
      )}

      {!buttonPressed && (
        <Protected>
          <button onClick={createNewCommit}>Commit files</button>
        </Protected>
      )}
      {buttonPressed && (
        <Protected>
          <NewCommit setButton={setButtonPressed} refreshRepos={refreshRepos} branchName={branchName}/>
        </Protected>
      )}
    </div>
  );
}
