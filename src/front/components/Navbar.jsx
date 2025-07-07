import { Link } from "react-router-dom";

export const Navbar = () => {

	return (
		<nav className="navbar bg-body-tertiary mb-5">
			<div className="container-fluid">
				<Link to="/">
					<img src="https://avatars.githubusercontent.com/u/202177717?v=4" alt="Logo" width="30" height="30" className="d-inline-block align-text-top rounded-3 mx-4"></img>
					<span className="navbar-brand mb-0 h1">JWT Token Front</span>
				</Link>
				<div className="ml-auto">
					<Link to="/signup">
						<button className="btn btn-primary m-2">Registrarse</button>
					</Link>
					<Link to="/login">
						<button className="btn btn-primary m-2">Iniciar sesion</button>
					</Link>
				</div>
			</div>
		</nav>
	);
};