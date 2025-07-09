import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { useLocation } from 'react-router-dom';

export const Navbar = () => {
  	const {store, dispatch} =useGlobalReducer();
	const location = useLocation();
	return (
		<nav className="navbar bg-body-tertiary mb-2">
			<div className="container-fluid">
				<Link to="/">
					<img src="https://avatars.githubusercontent.com/u/202177717?v=4" alt="Logo" width="30" height="30" className="d-inline-block align-text-top rounded-3 mx-4"></img>
					<span className="navbar-brand mb-0 h1">JWT Token Front</span>
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
							<Link to="/userprofile/me"> <span className="me-2"> <i className="fa-solid fa-user display-6 me-2"></i>{store.user} </span> </Link>
					)
				}
				</div>
			</div>
		</nav>
	);
};