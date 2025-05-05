import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await API.post("/auth/login", form);
      localStorage.setItem("token", res.data.token);
      navigate("/");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="flex flex-col gap-4 w-80 mx-auto mt-20">
      <h2 className="text-xl font-bold text-center">Login</h2>
      <input
        className="p-2 border rounded"
        placeholder="Username"
        value={form.username}
        onChange={(e) => setForm({ ...form, username: e.target.value })}
      />
      <input
        className="p-2 border rounded"
        placeholder="Password"
        type="password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <button className="bg-blue-500 text-white p-2 rounded" onClick={handleLogin}>
        Login
      </button>
    </div>
  );
}
