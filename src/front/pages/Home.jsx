import React, { useEffect,useState } from "react"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { getHello } from "../services/api";

export const Home = () => {
	const { store, dispatch } = useGlobalReducer()


	//JWT:Variables
	const [user,setUser] = useState(localStorage.getItem("user") || null);
	const [token, setToken] = useState(localStorage.getItem("token") || null);
	const [message, setMessage] = useState(localStorage.getItem("message") || null);
	//JWT:Logout
	const handleLogout = () => {
		setUser(null);
		setToken(null);
		setMessage(null);
		dispatch({type:"token", payload:"" });
		dispatch({type:"user", payload:"" });
		dispatch({type:"message", payload:"" });
		localStorage.removeItem("user");
		localStorage.removeItem("token");localStorage.removeItem("message");

	}
    const loadSession = () => {
		const lsToken=localStorage.getItem("token");
		const lsUser=localStorage.getItem("user");
		if(lsToken){
			dispatch({type:"token", payload:lsToken });
			dispatch({type:"user", payload:lsUser});
			setToken(lsToken);
			setUser(lsUser);
			return true;
		}
	return false;
	}

	const loadMessage = async () => {
		if(token && !message){
			try {
				const data=await getHello(token);
				dispatch({ type: "message", payload: await data?.message })
				setMessage(await data?.message)
				localStorage.setItem("message", await data?.message);
			} catch (error) {
				if (error.message) throw new Error(
					"Could not fetch the message from the backend. Please check if the backend is running and the backend port is public " + error
				);
			}
		}
	}

	useEffect(() => {
		loadSession();
		loadMessage();
	}, [token])
	return (
		<div className=" mt-2">
		{ token ? (
			<div className="alert alert-info">
					{message ? (
						<p className="text-success text-center mb-5">{message}</p>
					) : ( <> 
						<div className="text-center spinner-border text-primary" role="status"></div> 
							<span className="text-danger text-center">
								Loading message from the backend (make sure your python 🐍 backend is running)...
							</span>
						</>
					)}
          			{user && <p className="text-left">Usuario: {user}</p>}
					{token && <p className="text-left">Token: {token}</p>}
          			<button className="btn btn-secondary my-1 w-100" onClick={handleLogout}>Logout</button>
				</div>
				
				) : (
					<>
					<div className="container">	
							<p>Bienvenido a la Home inicia sesion para comenzar</p>
							<hr />
					</div>
					</>
				)
			}
		</div>
	);
}; 