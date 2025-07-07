import React, { useState } from "react";
import { registerUser } from "../services/api";

export const RegisterForm = ({ setToken }) => {
  const [form, setForm] = useState({ username: "", password: "", email: "" });
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await registerUser(form);
    const data = await res;

     if (res.ok) {
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
    } else {
      setMessage(data.msg);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Registro</h2>
      <div className="form-group">
        <label for="user">Usuario</label>
        <input placeholder="Usuario" id="user" onChange={(e) => setForm({ ...form, username: e.target.value })} />
      </div>
      <div className="form-group">
        <label for="password">Contraseña</label>
        <input type="password" placeholder="Contraseña" id="passsword" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      </div>
      <div className="form-group">
        <label for="email">Correo Electronico</label>
        <input type="email" placeholder="email" id="email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      </div>
      <button type="submit">Registrarse</button>
      {message && <p>{message}</p>}
    </form>
  );
}

export default RegisterForm;
