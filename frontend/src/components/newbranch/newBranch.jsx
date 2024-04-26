import React, { useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export default function NewBranch({ currentBranchName, setButton, setSelectedBranch , refreshBranches }) {
  const [newBranchName, setNewBranchName] = useState("");
  const { username, repoName } = useParams();

  const handleCancel = () => {
    setButton(false);
  };

  const createBranch = async () => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/branch/${username}/${repoName}/new`,
        { old_branch_name: currentBranchName, new_branch_name: newBranchName },
        { headers: { "Content-Type": "application/json" } }
      );
      console.log("New branch created:", response.data);
      setButton(false)
      refreshBranches()
      setSelectedBranch(newBranchName)
    } catch (error) {
      console.error("Failed to create new branch:", error);
      // Handle error, e.g., show an error message or alert
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="New Branch Name"
        value={newBranchName}
        onChange={(e) => setNewBranchName(e.target.value)}
      />
      <button onClick={handleCancel}>Cancel</button>
      <button onClick={createBranch}>Create Branch</button>
    </div>
  );
}
