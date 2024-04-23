import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

//TODO refresh 
//TODO fix backend stuff : Empty files, current branch and stuff
//TODO add current branch to repository
//TODO add get commit message to here


export default function NewCommit({ setButton }) {
  const [files, setFiles] = useState([]);
  const { username, repoName } = useParams();

  const handleCancel = () => {
    setButton(false);
  };

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("commit_message", "your_commit_message_here");
    files.forEach((file) => {
      formData.append("files", file);
    });

    axios
      .post(`http://127.0.0.1:8000/commit/${username}/${repoName}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("API response:", response.data);
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
      {files.length === 0 ? (
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
          <button onClick={handleSubmit}>Submit</button>
        </div>
      )}
      <button onClick={handleCancel}>Cancel</button>
    </div>
  );
}
