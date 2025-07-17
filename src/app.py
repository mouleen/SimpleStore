"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db,User
from api.base import api
from api.routes.images import routes_image
from api.routes.stores import routes_store
from api.routes.users import routes_user
from api.routes.products import routes_product
from api.routes.menus import routes_menu
from api.routes.userpoints import routes_userpoint
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager,create_access_token



# Environment
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')
app = Flask(__name__)

# Configuración de extension Flask-JWT-Extended 
app.config["JWT_SECRET_KEY"] = "madeinUSA"  
jwt = JWTManager(app)

app.url_map.strict_slashes = False

# Confguración de base de datos 
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)



app.register_blueprint(routes_image) # /api/images
app.register_blueprint(routes_store) # /api/stores
app.register_blueprint(routes_user) # /api/users
app.register_blueprint(routes_product) # /api/product
app.register_blueprint(routes_menu) # /api/menu
app.register_blueprint(routes_userpoint) # /api/userpoint
# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')


# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
