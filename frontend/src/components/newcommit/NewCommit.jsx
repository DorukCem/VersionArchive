import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";


export default function NewCommit({ setButton , refreshRepos, branchName }) {
  const [files, setFiles] = useState([]);
  const { username, repoName } = useParams();
  const [commitMessage, setCommitMessage] = useState("");

  const handleCancel = () => {
    setButton(false);
  };

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("commit_message", commitMessage);
    files.forEach((file) => {
      formData.append("files", file);
    });

    axios
      .post(`http://127.0.0.1:8000/commit/${username}/${repoName}/${branchName}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("API response:", response.data);
        refreshRepos()
        setButton(false);
      })
      .catch((error) => {
        console.error("API error:", error);
        // Handle error
      });
  };

  const handleDropFile = (event) => {
    event.preventDefault();
    const items = event.dataTransfer.items;
    const fileList = [];
    for (let i = 0; i < items.length; i++) {
      const entry = items[i].webkitGetAsEntry();
      if (entry.isFile) {
        fileList.push(new Promise((resolve) => entry.file(resolve)));
      } else if (entry.isDirectory) {
        fileList.push(traverseDirectory(entry, entry.name + "/"));
      }
    }
    Promise.all(fileList).then((files) => {
      setFiles(files.flat(100));
    });
  };
  const traverseDirectory = (directory, currentPath) => {
    return new Promise((resolve) => {
      const reader = directory.createReader();
      const fileList = [];
      const readEntries = () => {
        reader.readEntries((entries) => {
          entries.forEach((entry) => {
            if (entry.isFile) {
              fileList.push(
                new Promise((resolve) =>
                  entry.file((file) => {
                    // Modify the file name here before resolving
                    const modifiedFile = new File(
                      [file],
                      currentPath + file.name,
                      { type: file.type }
                    );
                    resolve(modifiedFile);
                  })
                )
              );
            } else if (entry.isDirectory) {
              fileList.push(
                Promise.resolve(
                  traverseDirectory(entry, currentPath + entry.name + "/")
                )
              );
            }
          });
          if (entries.length > 0) {
            readEntries();
          } else {
            resolve(Promise.all(fileList));
          }
        });
      };
      readEntries();
    });
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  useEffect(() => {
    console.log("Dropped files:", files);
  }, [files]);

  return (
    <div>
      {(files.length === 0) ? (
        <div
          onDrop={handleDropFile}
          onDragOver={handleDragOver}
          style={{
            border: "2px dashed #ccc",
            padding: "20px",
            textAlign: "center",
          }}
        >
          <p>Drag files here to upload:</p>
          
        </div>
      ) : (
        <div>
          <ul>
            {Array.from(files).map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul> 
          
        </div>
      )}
      <input
            type="text"
            value={commitMessage}
            onChange={(e) => setCommitMessage(e.target.value)}
            placeholder="Enter commit message"
          />
      <button onClick={handleCancel}>Cancel</button>
      {(files.length>0 && commitMessage!=="") && <button onClick={handleSubmit}>Submit</button>}
    </div>
  );
}
