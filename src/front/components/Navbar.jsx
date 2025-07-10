import { Link, Navigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { useLocation,useNavigate } from 'react-router-dom';

//import {handleGlobalLogout} from "../helpers/Helpers.jsx"
import { useGlobalHelpers } from "../hooks/useGlobalHelpers";
export const Navbar = () => {
  	const {store, dispatch} =useGlobalReducer();
	const location = useLocation();
	
	const navigate = useNavigate();
	const { logoutUser } = useGlobalHelpers();
	const handleLogout = ()=>{
		logoutUser();
		navigate('/login');
	}
	return (
		<nav className="navbar bg-body-tertiary mb-2 bg-black">
			<div className="container-fluid">
				<Link className="text-decoration-none link-warning" to="/">
					<img className="d-inline-block rounded-3 mx-4 mb-2" src="https://avatars.githubusercontent.com/u/202177717?v=4" alt="Logo" width="30" height="30" ></img>
					<span className="navbar-brand mb-0 mt-3 h1 text-dark">Simple Basic Store</span>
				</Link>
				<div className="ml-auto">
					{ !store?.token ? (
						<>
							 { (location.pathname !== '/signup') && ( 
								<Link to="/signup">
									<button className="btn btn-warning m-2">Registrarse </button>
								</Link>
							 )} 
							{ (location.pathname !== '/login') && (
								<Link to="/login">
									<button className="btn btn-warning m-2">Iniciar sesión </button>
								</Link>
							)}

						</>
					):( 
						<>
							<button className="btn btn-warning m-2" onClick={()=>{handleLogout()}}>Cerrar sesión </button>
							<Link className="text-decoration-none link-success" to="/userprofile/me"> <span className="me-2 "> <i className="fa-solid fa-user display-6 me-2 custom-fg-brown"></i>{store.user} </span> </Link>
						</>
					)
				}
				</div>
			</div>
		</nav>
	);
};