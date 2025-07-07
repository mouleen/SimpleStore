import React, { useState } from "react";
import { getToken } from "../services/api";

export const LoginForm = ({ setToken }) => {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await getToken(form);
    const data = await res;
    if (res.ok) {
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
    } else {
      setError(data.msg);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input placeholder="Usuario" onChange={(e) => setForm({ ...form, username: e.target.value })} />
      <input type="password" placeholder="Contraseña" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button type="submit">Entrar</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

export default LoginForm;