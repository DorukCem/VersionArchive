import { useState, useEffect } from "react";
import { NavLink, useParams } from "react-router-dom";
import Protected from "../../components/protected/protected";
import NewCommit from "../../components/newcommit/NewCommit";
import Commit from "../commit/commit";
import "./branchpage.css";

export default function Branch({ branchName, setRepoNotFound }) {
  const { username, repoName } = useParams();
  const [buttonPressed, setButtonPressed] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [branchData, setBranchData] = useState(null);
  const [commits, setCommits] = useState([]);
  const [selectedCommit, setSelectedCommit] = useState(null);
  const [showCommits, setShowCommits] = useState(false);

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
          setSelectedCommit(data.head_commit_id);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    async function fetchCommits() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/branch/${username}/${repoName}/${branchName}/commits`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch commits in branch");
        } else {
          const data = await response.json();
          setCommits(data);
        }
      } catch (error) {
        console.error(error);
      }
    }

    fetchBranchContents();
    fetchCommits();
  }, [repoName, branchName, refresh]);

  const createNewCommit = () => {
    setButtonPressed(true);
  };

  const refreshRepos = () => {
    setRefresh(refresh + 1);
  };

  const toggleShowCommits = () => {
    setShowCommits(!showCommits);
  };

  const handleCommitClick = (commit_id) => {
    setSelectedCommit(commit_id);
  };

  function formatDateTime(dateTimeString) {
    const dateTime = new Date(dateTimeString);
    const options = {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    };
    return dateTime.toLocaleDateString("en-US", options);
  }

  // Some things can only be done on head commit and others only on previous commits such as reset()
  function is_head_commit() {
    return (
      selectedCommit === null || selectedCommit === branchData.head_commit_id
    );
  }

  async function handleReset() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/branch/${username}/${repoName}/${branchName}/reset/${selectedCommit}`,
        {
          method: "PUT",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to reset branch");
      } else {
        // Handle successful reset
        refreshRepos();
      }
    } catch (error) {
      console.error(error);
      // Handle error (e.g., display an error message)
    }
  }

  return (
    <div className="branch-container">
      {branchData && branchData.head_commit_id ? (
        <Commit
          branchName={branchName}
          commit_id={selectedCommit || branchData.head_commit_id}
          setRepoNotFound={setRepoNotFound}
        />
      ) : branchData !== null ? (
        <span className="placeholder">This branch does not have a commit</span>
      ) : null}

      {!buttonPressed && (
        <div>
          <div className="buttons">
            <div>
              <button
                className="prev-commits-button"
                onClick={toggleShowCommits}
              >
                {showCommits
                  ? "Hide previous commits"
                  : "View previous commits"}
              </button>
            </div>

            {is_head_commit() && (
              <div>
                <Protected>
                  <button className="commit-button" onClick={createNewCommit}>
                    Commit new files
                  </button>
                </Protected>
              </div>
            )}
          </div>

          {showCommits && (
            <div className="showcommit-container">
              <span className="showcommit__title">
                Commits in{" "}
                <span className="showcommit__title-branchname">
                  {branchName}
                </span>
              </span>
              <ul className="showcommit-list">
                {commits.map((commit, index) => (
                  <li
                    key={index}
                    onClick={() => handleCommitClick(commit.id)}
                    style={{ cursor: "pointer" }}
                    className="showcommit__li"
                  >
                    <div
                      className={
                        commit.id === selectedCommit
                          ? "selected-commit showcommit-item"
                          : "showcommit-item"
                      }
                    >
                      <div className="commit__header">
                        <span>{`ID: ${commit.oid.substring(0, 8)}`}</span>
                        <span>{`${formatDateTime(commit.timestamp)}`}</span>
                      </div>
                      <div className="commit__footer">
                        <span className="commitmessage">{`${commit.commit_message}`}</span>
                        <div style={{display: "flex", alignItems: "end", justifyContent: "end"}}>
                          <div className="reset__button__container">
                            {commit.id === selectedCommit &&
                              !is_head_commit() && (
                                <Protected>
                                  <button
                                    className="reset-button"
                                    onClick={handleReset}
                                  >
                                    Reset branch
                                  </button>
                                </Protected>
                              )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      {buttonPressed && (
        <Protected>
          <NewCommit
            setButton={setButtonPressed}
            refreshRepos={refreshRepos}
            branchName={branchName}
          />
        </Protected>
      )}
    </div>
  );
}
