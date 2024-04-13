import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./vc-object.css";

export default function VCObject() {
  const { username, repoName, oid } = useParams();
  const [objectData, setObjectData] = useState({});
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    async function fetchObjectData() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/object/${username}/${repoName}/${oid}`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setNotFound(true);
          } else {
            throw new Error("Failed to fetch object data");
          }
        } else {
          const data = await response.json();
          setObjectData(data);
          setNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setNotFound(true);
      }
    }
    fetchObjectData();
  }, [username, repoName, oid]);

  if (notFound) {
    return <div>Object not found</div>;
  }
  console.log(objectData.blob);

  return (
    <div className="App">
      <h1>{objectData.name}</h1>
      <div className="display-linebreak">
        <p>{objectData.blob}</p>
      </div>
    </div>
  );
}
