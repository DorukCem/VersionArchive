import { useState, useEffect } from "react";
import { NavLink, useParams } from "react-router-dom";
import Protected from "../../components/protected/protected";
import NewCommit from "../../components/newcommit/newCommit";
import Commit from "../commit/commit";

export default function Branch({ branchName, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [buttonPressed, setButtonPressed] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [branchData, setBranchData] = useState(null) 

  useEffect(() => {
    async function fetchBranchContents() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/branch/${username}/${repoName}/${branchName}`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setRepoNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setBranchData(data);
          setRepoNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    fetchBranchContents();
  }, [repoName, branchName, refresh]);

  const createNewCommit = () => {
    setButtonPressed(true);
  };

  const refreshRepos = () => {
    setRefresh(refresh + 1);
  };

  return (
    <div className="App">
      {branchData && branchData.head_commit_oid ? <Commit branchName={branchName} commit_oid={branchData.head_commit_oid} setRepoNotFound={setRepoNotFound}/> : <h1>This branch does not have a commit</h1>}

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
