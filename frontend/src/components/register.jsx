import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await API.post("/auth/register", form);
      alert("User registered!");
      navigate("/login");
    } catch {
      alert("User already exists");
    }
  };

  return (
    <div className="flex flex-col gap-4 w-80 mx-auto mt-20">
      <h2 className="text-xl font-bold text-center">Register</h2>
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
      <button className="bg-green-600 text-white p-2 rounded" onClick={handleRegister}>
        Register
      </button>
    </div>
  );
}
