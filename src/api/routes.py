"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
import json,yaml

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Endpoint de Validacion de Seguridad para pruebas
@api.route('/private', methods=['POST', 'GET'])
@api.route('/hello', methods=['POST', 'GET'])
@jwt_required()
def handle_hello():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    response_body = {
        "message": f"Hola {user.username}! Bienvenido gracias por ingresar tus credenciales",
        "ok":True
    }
    return jsonify(response_body), 200

# Endpoint de Registracion
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
        return jsonify({"msg": "No es posible crear un usuario con esos datos"}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    return jsonify(access_token=access_token, username=username, ok=True, msg="Usuario creado con exito"), 201

@api.route("/admin/users",methods=["GET"])
def test():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Endpoint de Logout
@api.route("/login", methods=["POST"])
@api.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
   
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token, username=user.username, ok=True ), 200
