import React, { useState } from "react";
import { registerUser } from "../services/api";
import { useNavigate } from 'react-router-dom';
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const RegisterForm = ({ setToken }) => {
  const [form, setForm] = useState({ username: "", password: "", email: "" });
  const [message, setMessage] = useState("");
  const [hasAuth,setHasAuth]= useState(false);
  const [loading, setLoading] = useState(true);
  const {store, dispatch} =useGlobalReducer()
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await registerUser(form);
    if (res.ok) {
      setForm({ username: "", password: "", email: "" });
      setMessage("Registración existosa");
      setTimeout(() => {
        navigate("/login"); 
       }, 200); // segundos
    } else {
      setMessage(res.msg);
    }
  };

  return (
    <div className="row text-center">
      <div className="col-12 offset-2">
        <form className="my-1 py-1 mx-5 px-5 w-50" onSubmit={handleSubmit} >
          <h4>Registro</h4>
          <div className="form-group">
            <label htmlFor="user">Usuario</label>
            <input className="form-control" placeholder="Usuario" id="user" onChange={(e) => setForm({ ...form, username: e.target.value })} />
          </div>
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input className="form-control" type="password" placeholder="Contraseña" id="passsword" onChange={(e) => setForm({ ...form, password: e.target.value })} />
          </div>
          <div className="form-group">
            <label htmlFor="email">Correo Electronico</label>
            <input className="form-control" type="email" placeholder="email" id="email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
          </div>
          <button className="btn btn-secondary my-2 w-100" type="submit">Registrarse</button>
          {message && <p>{message}</p>}
        </form>
      </div>
    </div>
  );
}

export default RegisterForm;
