import React, { useEffect,useState } from "react"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import RegisterForm from "../components/RegisterForm.jsx";
import LoginForm from "../components/Loginform.jsx";
import { useNavigate } from 'react-router-dom';
import { getToken,getHello } from "../services/api";

export const Home = () => {
	const { store, dispatch } = useGlobalReducer()
	const navigate = useNavigate();
	

	//JWT:Variables
	const [user,setUser] = useState(null);
	const [token, setToken] = useState(null);
	//JWT:Logout
	const handleLogout = () => {
		setUser(null);
		setToken(null);
		dispatch({type:"get_token", payload:"" });
		dispatch({type:"get_user", payload:"" });
		localStorage.removeItem("user");
		localStorage.removeItem("token");
		navigate('/login')
	}
    const loadSession = async () => {
		try {
			const lsToken=localStorage.getItem("token");
			if(lsToken){
				dispatch({type:"get_token", payload:lsToken });
				setToken(lsToken);
				return true;
			}
		} catch (error) {
			if (error.message) throw new Error(
				"Could not fetch the message from the backend. Please check if the backend is running and the backend port is public " + error
			);	
		}
	return false;
	}

	const loadMessage = async () => {
		try {
			if(token){
				const data=await getHello(token);
				dispatch({ type: "set_hello", payload: data.message })
			}
		} catch (error) {
			if (error.message) throw new Error(
				"Could not fetch the message from the backend. Please check if the backend is running and the backend port is public " + error
			);
		}
	}

	useEffect(() => {
		//JWT:UseEffect
		loadSession();
		loadMessage();
	}, [])

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
							{/* <RegisterForm setToken={setToken} /> */}
							<hr />
							<LoginForm />
					</div>
					</>
				)
			}
		</div>
	);
}; 