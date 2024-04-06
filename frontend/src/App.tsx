import './App.css'
import { useState, useEffect } from 'react';


export default function App() {
  const [repositories, setRepositories] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/Doruk/all-repos')
      .then(response => response.json())
      .then(data => setRepositories(data))
      .catch(error => console.error('Error fetching repositories:', error));
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold underline">
        Hello world!
      </h1>
      <h2 className="text-xl font-bold mt-4">User Repositories:</h2>
      <ul>
        {repositories.map(repo => (
          <li key={repo}>{repo}</li>
        ))}
      </ul>
    </div>
  );
}