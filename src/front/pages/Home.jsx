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
		dispatch({type:"get_token", payload:"" });
		dispatch({type:"get_user", payload:"" });
		dispatch({type:"get_hello", payload:"" });
		localStorage.removeItem("user");
		localStorage.removeItem("token");

	}
    const loadSession = () => {
		const lsToken=localStorage.getItem("token");
		const lsUser=localStorage.getItem("username");
		if(lsToken){
			dispatch({type:"get_token", payload:lsToken });
			dispatch({type:"get_user", payload:lsUser});
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
				dispatch({ type: "get_hello", payload: await data?.message })
				setMessage(await data?.message)
				localStorage.setItem("user", await data?.message);
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
		<div className="text-center mt-2">
		{ token ? (
				<div className="alert alert-info">
					{store.message ? (
						<span>{store.message}</span>
					) : ( 
						<span className="text-danger">
							Loading message from the backend (make sure your python 🐍 backend is running)...
						</span>
					)}
					<p>Token: {token}</p>
          			<button className="btn btn-secondary my-1 w-100" onClick={handleLogout}>Logout</button>
          			{user && <p>Usuario: {user}</p>}
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