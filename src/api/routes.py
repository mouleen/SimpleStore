"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User, Store,Image,Product,UserPoint,Menu,Category
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
    passsword_validate = data.get("password_validate")

    if  password != passsword_validate:
        return jsonify({"msg":f"Las contraseñas no son iguales","ok":False}), 400

    if not username or not email or not password:
        return jsonify({"msg": "Datos incompletos","ok":False}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "No es posible crear un usuario con esos datos","ok":False}), 409

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
        return jsonify({"msg": "Credenciales inválidas","ok":False}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token, username=user.username, ok=True ), 200



## STORES ##
# Endpoint de creacion de tienda
@api.route('/store/create', methods=['POST'])
@jwt_required()
def store_create():
    body=json.loads(request.data)
    if body is None or len(body['nombre']) < 1 or len(body['direccion']) < 1 :
        return {"msg": "Los datos enviados no son suficientes"}, 400
    if Store.query.filter((Store.nombre == body['nombre']) | (Store.direccion == body['direccion'])).first():
        return jsonify({"msg": "No es posible crear una tienda con esos datos"}), 409
    current_user_id = get_jwt_identity()
    #user = User.query.get(current_user_id)
    local_store= Store()
    local_store.nombre=body['nombre']
    local_store.user_id=current_user_id
    local_store.direccion=body['direccion']
    db.session.add(local_store)
    db.session.commit()
    return body

@api.route('/admin/stores/list', methods=['GET'])
@jwt_required()
def stores_list():
    stores = Store.query.all()
    return jsonify([store.serialize() for store in stores]), 200

## IMAGES ##
# Endpoint de creacion de tienda
@api.route('/image/create', methods=['POST'])
@jwt_required()
def add_image():
    body=json.loads(request.data)
    owner_type=body['owner_type']
    owner_id=body['owner_id']
    name=body['name']
    img_type=body['img_type']
    url=body['url']
    position=body['position']
    
    # Validar tipo de entidad
    valid_types = ['store', 'product', 'user']
    if owner_type not in valid_types:
        raise ValueError(f"Tipo no válido. Debe ser uno de: {valid_types}")
    

    # Validar que el objeto exista antes de asignarlo
    model_map = {
        'store': Store,
        'product': Product,
        'user': User
    }

    entity_model = model_map.get(owner_type)
    if not db.session.get(entity_model, owner_id):
        raise ValueError(f"{owner_type.capitalize()} con ID {owner_id} no existe.")
    
    # solo aceptamos una imagen index
    if img_type == 'index':
        existing_index = Image.query.filter_by(owner_type=owner_type,owner_id=owner_id,type='index').first()git statuu
        if existing_index:
            return jsonify({"msg":f"Ya existe una imagen de tipo 'index' para {owner_type} con ID {owner_id}.","ok":False})

    # Crear imagen
    image = Image(
        owner_type=owner_type,
        owner_id=owner_id,
        name=name,
        type=img_type,
        url=url,
        position=position
    )

    db.session.add(image)
    db.session.commit()
    return image.serialize()

@api.route("/images/<string:entity_type>/<int:entity_id>", methods=["GET"])
@jwt_required()
def get_images_for(entity_type: str, entity_id: int):
    return Image.query.filter_by(owner_type=entity_type, owner_id=entity_id).all()



@api.route('/admin/images/list', methods=['GET'])
@jwt_required()
def images_list():
    images = Image.query.all()
    return jsonify([image.serialize() for image in images]), 200

@api.route("/images/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_image_for(id: int):
    image_exists=Image.query.filter_by(id=id).first()
    if not image_exists:
            return jsonify({"msg":f"No existe una imagen con ID {id}.","ok":False}) , 400
    
    db.session.delete(image_exists)
    db.session.commit()
    return jsonify({"msg":"Imagen eliminada con exito","ok":True})

    


