import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";


export default function Repository(){
  const { username, repoName } = useParams();
  const [objects, setObjects] = useState([]);
  const [repoNotFound, setRepoNotFound] = useState(false);

  useEffect(() => {
    async function fetchRepoContents() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/object/${username}/${repoName}/all`
        );
        if (!response.ok) {
          if (response.status === 404) {
            setRepoNotFound(true);
          } else {
            throw new Error("Failed to fetch user's repositories");
          }
        } else {
          const data = await response.json();
          setObjects(data);
          setRepoNotFound(false);
        }
      } catch (error) {
        console.error(error);
        setRepoNotFound(true);
      }
    }
    fetchRepoContents();
  }, [repoName]);

  if (repoNotFound) {
    return <div>Repository does not exist</div>;
  }

  return (
    <div className="App">
      <h1>{repoName}'s contents</h1>
      <ul>
        {objects.map((obj) => (
          <li key={obj.id}>{obj.name}</li>
        ))}
      </ul>
    </div>
  );
}
