import { BrowserRouter, Routes, Route } from "react-router-dom";
import Chat from "./components/chat";
import Login from "./components/login";
import Register from "./components/register";

function App() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={token ? <Chat /> : <Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
