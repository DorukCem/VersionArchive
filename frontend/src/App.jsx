import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/navbar";
import Home from "./pages/home";
import Tutorial from "./pages/tutorial";
import UserProfile from "./pages/user/userpage";
import Repository from "./pages/repository/repository";
import VCObject from "./pages/vc-object";
import Login from "./pages/login/login";
import SignUp from "./pages/signup/signup";

function App() {
  return (
    <div>
      <div className="min-h-screen p-6 bg-white text-gray-600 text-large">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tutorial" element={<Tutorial />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/:username" element={<UserProfile />} />
          <Route path="/:username/:repoName" element={<Repository />} />
          <Route
            path="/:username/:repoName/object/:oid"
            element={<VCObject />}
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
