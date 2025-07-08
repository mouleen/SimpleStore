import React, { useState,useEffect } from "react";
import { getToken } from "../services/api";
import { useNavigate } from 'react-router-dom';
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const LoginForm = ({ setToken }) => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [hasAuth,setHasAuth]= useState(false);
  const [loading, setLoading] = useState(true);
  const {store, dispatch} =useGlobalReducer();

  const handleLogout = () => {
    setLoading(true);
		setHasAuth(false);
		localStorage.removeItem("user");
		localStorage.removeItem("token");
    dispatch({type:"get_token", payload:"" });
    setLoading(false);
    navigate('/login')
	}

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await getToken(form); 
    if (res.ok) {
      //setToken(data.access_token);
      localStorage.setItem("token", res.access_token);
      localStorage.setItem("user", res.username);
      dispatch({type:"get_token", payload:res.access_token });
      dispatch({type:"get_user", payload:res.username });
      setHasAuth(true);
      setLoading(true);
		  //setToken(store.token);
      console.log("TOKEN=",store.token);
      if (location.pathname !== '/') {
        navigate('/'); 
      }
    } else {
		  //localStorage.removeItem("user");
		  localStorage.removeItem("token");
      dispatch({type: "get_token",payload: "" });
      console.log("TOKEN=",store.token)
      setHasAuth(false);
      setLoading(false);
      setError(res.msg);
    }
  };
  useEffect(() => {
    const lsToken=localStorage.getItem("token");
		if(lsToken){
      setHasAuth(true);
      setLoading(false);
      dispatch({type: "get_token",payload: lsToken });

      const timer = setTimeout(() => {
        setLoading(false);
        navigate("/"); 
      }, 200); // segundos
  
      return () => clearTimeout(timer); // limpieza
		}
  },[navigate,hasAuth,loading])
  return (
    <div className="row text-center">
      { loading && hasAuth ? (
          <div className="col-12">
            <div className="text-center spinner-border text-primary" role="status">
              <span className="visually-hidden">Cargando...</span>
            </div>
            <p>Sesión iniciada en breve seras redirigido</p>
          </div>
        ) : (
           !hasAuth ? ( 
            <div className="row text-center">
              <div className="col-12 offset-2">
                <form className="my-1 py-1 mx-5 px-5 w-50" onSubmit={handleLogin}>
                  <h4>Login</h4>
                  <label htmlFor="newuser">Usuario</label>
                  <input id="newuser"className="form-control" placeholder="Usuario" onChange={(e) => setForm({ ...form, username: e.target.value })} />
                  <label htmlFor="newpassword">Contraseña</label>
                  <input id="newpassword" className="form-control" type="password" placeholder="Contraseña" onChange={(e) => setForm({ ...form, password: e.target.value })} />
                  <button className="btn btn-secondary my-2 w-100" type="submit">Entrar</button>
                  {error && <p style={{ color: "red" }}>{error}</p>}
                </form>
              </div>
            </div>
          ) : (  
          <div className="col-12">
            <div className="text-center spinner-border text-primary" role="status">
            </div>
            <button className="btn btn-secondary my-1 w-100" onClick={handleLogout}>Logout</button> 
            <p>sesion iniciada en breve seras redirigido</p>
          </div>
        ))
      }
    </div>
  );
}

export default LoginForm;