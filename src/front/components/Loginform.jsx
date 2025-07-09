import React, { useState,useEffect } from "react";
import { getToken } from "../services/api";
import { useNavigate } from 'react-router-dom';
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { useLocation } from 'react-router-dom';

export const LoginForm = ({ setToken }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [hasAuth,setHasAuth]= useState(false);
  const [loading, setLoading] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const {store, dispatch} =useGlobalReducer();

  const handleLogout = () => {
    setLoading(true);
		setHasAuth(false);
		localStorage.removeItem("user");
		localStorage.removeItem("token");
    localStorage.removeItem("message");
    dispatch({type:"set_token", payload:"" });
    dispatch({type:"get_helo", payload:"" });
    dispatch({type:"get_user", payload:"" });
    setLoading(false);
    navigate('/login')
	}

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await getToken(form); 
    if (res.ok) {
      //setToken(data.access_token);
      localStorage.setItem("token", await res?.access_token);
      localStorage.setItem("user", await res?.username);
      dispatch({type:"get_token", payload:await res.access_token });
      dispatch({type:"get_user", payload:await res.username });
      setHasAuth(true);
      setLoading(false);
      setError("un exito");
      if (location.pathname !== '/') {
        navigate('/'); 
      } 
    } else {
      setHasAuth(false);
      setLoading(false);
      setError('ERROR - '+res?.msg );
    }
  };
  useEffect(() => {
    const lsToken=localStorage.getItem("token");
		if(lsToken){
      setHasAuth(true);
      setLoading(false);
      const lsUser=localStorage.getItem("user");
      dispatch({type: "get_token",payload: lsToken });
      dispatch({type: "get_user",payload: lsUser });
		}else{setHasAuth(false);}
  },[navigate,hasAuth])
  return (
    <div className="container container-style bg-white rounded-4 w-50 shadow ">   
        { (!hasAuth ? ( 
              <div className="row justify-content-center text-center">
                <div className="col-md-10 col-lg-10">
                  <form className="my-1 py-1 px-4" onSubmit={handleLogin}>
                    <i className="fa-solid fa-mug-hot display-6 my-3"></i>
                    <h2>CoffeeConnect</h2>
                    <div className="input-group my-4">
                      <span className="input-group-text"><i className="fas fa-envelope"></i></span>
                      <input id="newuser"className="form-control" placeholder="Usuario" onChange={(e) => setForm({ ...form, username: e.target.value })} />
                    </div>
                     <div className="input-group my-4">
                        <span className="input-group-text"><i className="fas fa-lock"></i></span>
                        <input id="newpassword" className="form-control" type={showPassword ? 'text' : 'password'} placeholder="Contraseña" onChange={(e) => setForm({ ...form, password: e.target.value })} />
                        <button type="button" onClick={() => setShowPassword(!showPassword)}className="btn btn-link text-secondary position-absolute top-50 end-0 translate-middle-y me-2 p-0">
                            <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                        </button>
                    </div>
                    <button className="btn btn-warning my-2 w-100 text-white custom-brown" type="submit" >Iniciar sesion</button>
                    {error && <p style={{ color: "red" }}>{error}</p>}
                  </form>
                   <p>¿No tienes cuenta? <a className="text-decoration-none link-warning" href="">Regístrate</a> </p> 
                </div>
              </div>
            ) : (  
              <div className="col-12">
                <div className="text-center spinner-border text-primary" role="status">
                </div> 
                <button className="btn btn-secondary my-1 w-100" onClick={handleLogout}>Logout</button> 
                <p>sesion iniciada</p>
            </div>
          ))
        }

    </div>
  );
}

export default LoginForm;