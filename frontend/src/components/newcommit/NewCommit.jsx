import React, { useState, useEffect } from "react";

export default function NewCommit({ setButton }) {
  const [files, setFiles] = useState([]);

  const handleCancel = () => {
    setButton(false);
  };

  const handleSubmit = () => {
    setButton(false);
  };

  const handleDropFile = (event) => {
    event.preventDefault();
    setFiles(event.dataTransfer.files);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  useEffect(() => {
    console.log("Dropped files:", files);
  }, [files]);

  return (
    <div>
      {files.length===0 ? (
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