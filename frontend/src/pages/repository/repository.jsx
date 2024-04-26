  import { useState, useEffect } from "react";
  import { NavLink, useParams } from "react-router-dom";

  import Branch from "../../components/branch/branch";
  import NewBranch from "../../components/newbranch/newBranch";
  import Protected from "../../components/protected/protected";

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
            if (selectedBranch === "" ){
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
      <div>
        <h4>Repository {repoName}</h4>
        <select value={selectedBranch} onChange={handleBranchChange}>
          {branches.map((branch) => (
            <option key={branch} value={branch}>
              {branch}
            </option>
          ))}
        </select>
        <Protected><button onClick={handleCreateBranch}>Create new Branch</button></Protected>
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
    ) : (
      <div>Loading...</div>
    );
  }
