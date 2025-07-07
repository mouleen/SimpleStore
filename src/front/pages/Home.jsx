import React, { useEffect,useState } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import RegisterForm from "../components/RegisterForm.jsx";
import LoginForm from "../components/Loginform.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()
	//JWT:Variables
	const [user,setUser] = useState(null);
	const [token, setToken] = useState(null);
	//JWT:Logout
	const handleLogout = () => {
		setUser(null);
		setToken(null);
		localStorage.removeItem("user");
		localStorage.removeItem("token");
	}

	const loadMessage = async () => {
		try {
			const backendUrl = import.meta.env.VITE_BACKEND_URL

			if (!backendUrl) throw new Error("VITE_BACKEND_URL is not defined in .env file")
			const login = await fetch(backendUrl + "/api/login",
				{
					method:"POST",
					headers:{
						"content-type":"application/json"
					},
					body:JSON.stringify({
						"username":"traemesuerte2",
						"password":"madeinUSA321"
					})
				}
			)
			const datalogin = await login.json()
			let access_token=datalogin.access_token;

			if (datalogin.ok) {
				const response = await fetch(backendUrl + "/api/hello",
					{
						headers:{
							"Authorization":"Bearer "+ access_token
						}
					}
				)
				const data = await response.json()
	
				if (response.ok) dispatch({ type: "set_hello", payload: data.message })
			}

			return data

		} catch (error) {
			if (error.message) throw new Error(
				"Could not fetch the message from the backend. Please check if the backend is running and the backend port is public " + error
			);
		}
	}

	useEffect(() => {
		//JWT:UseEffect
		const localStorageUser= localStorage.getItem("user");
		if(localStorageUser){
			setUser(JSON.parse(localStorageUser));
		}
		loadMessage()
	}, [])

	return (
		<div className="text-center mt-5">
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
          			<button onClick={handleLogout}>Logout</button>
          			{user && <p>Usuario: {user}</p>}
				</div>
				
				) : (
					<>
					<RegisterForm setToken={setToken} />
					<hr />
					<LoginForm  setToken={setToken} />
					</>
				)
			}
		</div>
	);
}; 