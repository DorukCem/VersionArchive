import { useState, useEffect } from "react";
import { NavLink, useParams } from "react-router-dom";

import Branch from "../../components/branch/branch";
import NewBranch from "../../components/newbranch/newBranch";
import Protected from "../../components/protected/protected";
import "./repositorypage.css";

export default function Repository() {
  const { username, repoName } = useParams();
  const [branches, setBranches] = useState([]);
  const [repoNotFound, setRepoNotFound] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [selectedBranch, setSelectedBranch] = useState("");
  const [createBranchButton, setCreateBranchButton] = useState(false);

  useEffect(() => {
    async function fetchBranches() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/repo/${username}/${repoName}/all-branches`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setRepoNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setBranches(data);
          if (selectedBranch === "") {
            setSelectedBranch(data.length > 0 ? data[0] : "");
          }
          setRepoNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    fetchBranches();
  }, [repoName, refresh]);

  const refreshBranches = () => {
    setRefresh(refresh + 1);
  };

  const handleCreateBranch = () => {
    setCreateBranchButton(true);
  };

  if (repoNotFound) {
    return <div>Repository does not exist</div>;
  }

  const handleBranchChange = (e) => {
    setSelectedBranch(e.target.value);
  };

  return branches.length > 0 ? (
    <div className="page-container">
      <div className="repo-container">
        <div className="header">
          <div className="repo-title">
            <i className="bi bi-folder-fill"></i>
            <span className="repo-name">{repoName}</span>
          </div>
          <div className="edit-branch">
            <select
              className="select-branch"
              value={selectedBranch}
              onChange={handleBranchChange}
            >
              {branches.map((branch) => (
                <option key={branch} value={branch}>
                  {branch}
                </option>
              ))}
            </select>
            <Protected>
              <button className="create-branch" onClick={handleCreateBranch}>
                Create new Branch
              </button>
            </Protected>
          </div>
        </div>
        {!createBranchButton ? (
          selectedBranch && (
            <Branch
              branchName={selectedBranch}
              setRepoNotFound={setRepoNotFound}
            />
          )
        ) : (
          <Protected>
            <NewBranch
              currentBranchName={selectedBranch}
              setButton={setCreateBranchButton}
              refreshBranches={refreshBranches}
              setSelectedBranch={setSelectedBranch}
            />
          </Protected>
        )}
      </div>
    </div>
  ) : (
    <div>Loading...</div>
  );
}
