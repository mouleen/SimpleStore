import React, { useState } from "react";
import { registerUser } from "../services/api";
import { useNavigate } from 'react-router-dom';
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const RegisterForm = ({ setToken }) => {
  const [form, setForm] = useState({ username: "", password: "", email: "" });
  const [message, setMessage] = useState("");
  const [hasAuth,setHasAuth]= useState(false);
  const [loading, setLoading] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
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
    <div className="container container-style bg-white rounded-4 w-50 shadow mt-4">   
      <div className="row justify-content-center text-center">
        <div className="col-md-12 col-lg-12">
          <form className="my-1 py-1 mx-2 px-3" onSubmit={handleSubmit} >
            <i className="fa-solid fa-brain display-6 my-3 custom-fg-brown"></i>
            <h1 className="my-3">Codemind</h1>  
            {/* Campo de usuario */}
            <div className="input-group my-4">
              <span className="input-group-text"><i class="fa-solid fa-user"></i></span>
              <input className="form-control" placeholder="Usuario" id="user" onChange={(e) => setForm({ ...form, username: e.target.value })} />
            </div>
            {/* Campo de email */}
            <div className="input-group my-4">
              <span className="input-group-text"><i className="fas fa-envelope"></i></span>
              <input className="form-control" type="email" placeholder="Email" id="email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            {/* Campo de contrasena */}
            <div className="input-group my-4">
              <span className="input-group-text"><i className="fas fa-lock"></i></span>
              <input className="form-control" type={showPassword ? 'text' : 'password'} placeholder="Contraseña" id="passsword" onChange={(e) => setForm({ ...form, password: e.target.value })} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} className="btn btn-link text-secondary position-absolute top-50 end-0 translate-middle-y me-2 p-0">
                  <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
              </button>
            </div>
            {/* Campo de confirmar contrasena */}
            <div className="input-group my-4">
              <span className="input-group-text"><i className="fas fa-lock"></i></span>
              <input className="form-control" type={showPassword ? 'text' : 'password'} placeholder="Confirmar contraseña" id="passsword_validate" onChange={(e) => setForm({ ...form, password: e.target.value })} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} className="btn btn-link text-secondary position-absolute top-50 end-0 translate-middle-y me-2 p-0">
                  <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
              </button>
            </div>
            <button className="btn btn-secondary my-2 w-100 text-white custom-bg-brown my-4" type="submit">Crear Cuenta</button>
            {message && <p>{message}</p>}
             <p>¿Ya tienes cuenta? <a className="text-decoration-none link-warning custom-fg-brown mb-2" href="/login">Inicia Sesión</a> </p> 
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegisterForm;
