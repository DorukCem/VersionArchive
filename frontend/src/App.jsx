import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import Home from "./pages/home";
import Tutorial from "./pages/tutorial";

function App() {
  return (
    <div>
      <div className="min-h-screen p-6 bg-white text-gray-600 text-large">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tutorial" element={<Tutorial />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
