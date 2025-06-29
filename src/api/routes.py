"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager

api = Blueprint('api', __name__)
#api = Flask(__name__)
#api.config["JWT_SECRET_KEY"] = "madeinUSA"
#current_app.config["JWT_SECRET_KEY"] = "madeinUSA"  # Change this "super secret" to something else!

# Allow CORS requests to this API
CORS(api)

#jwt = JWTManager(api)
@api.route('/hello', methods=['POST', 'GET'])
@jwt_required()
def handle_hello():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    response_body = {
        "message": f"Hello {user}! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/register", methods=["POST"])
@api.route('/user/create', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "Datos incompletos"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "Usuario ya registrado"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    #return jsonify("msg":"trlalala")
    return jsonify(access_token=access_token, username=username), 201


@api.route("/listusers",methods=["GET"])
def test():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200