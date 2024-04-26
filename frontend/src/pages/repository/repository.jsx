import { useState, useEffect } from "react";
import { NavLink, useParams } from "react-router-dom";

import Branch from "../../components/branch/branch";


export default function Repository() {
  const { username, repoName } = useParams();
  const [branches, setBranches] = useState([]);
  const [repoNotFound, setRepoNotFound] = useState(false);
  const [refresh, setRefresh] = useState(0);
  const [selectedBranch, setSelectedBranch] = useState("");

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
          setSelectedBranch(data.length > 0 ? data[0] : ""); 
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

  if (repoNotFound) {
    return <div>Repository does not exist</div>;
  }

  const handleBranchChange = (e) => {
    setSelectedBranch(e.target.value);
  };
  
  return branches.length > 0 ? (
    <div>
      <h4>Current Branch: {selectedBranch}</h4>
      <select value={selectedBranch} onChange={handleBranchChange}>
        {branches.map((branch) => (
          <option key={branch} value={branch}>
            {branch}
          </option>
        ))}
      </select>
      {selectedBranch && (
        <Branch branchName={selectedBranch} setRepoNotFound={setRepoNotFound} />
      )}
    </div>
  ) : (
    <div>Loading...</div>
  );
}
