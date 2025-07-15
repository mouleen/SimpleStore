"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User, Store,Image,Product,UserPoint,Menu,Category
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
import json,yaml
from api.constants import ROLE_ADMIN

routes_image = Blueprint('images', __name__,url_prefix='/api/image')

# Allow CORS requests to this API
CORS(routes_image)

## IMAGES ##
# Endpoint ADMIN de listado de Imagenes
@routes_image.route('/admin/list', methods=['GET'])
@jwt_required()
def images_list_admin():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    images = Image.query.all()
    # Aramamos la respuesta
    response=jsonify({
        "msg": "Listado de Imagenes",
        "ok": True,
        "data": [image.serialize() for image in images]
    })
    

    return response,200

@routes_image.route('/list', methods=['GET'])
@jwt_required()
def images_list():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    images=Image.query.filter_by(user_id=user.id).all()

    # Aramamos la respuesta
    response=jsonify({
        "msg": f"Listado de Imagenes para {user.username}",
        "ok": True,
        "data": [image.serialize() for image in images]
    })
    

    return response,200


# Endpoint de creacion de Imagen
@routes_image.route('/admin/create', methods=['POST'])
@jwt_required()
def add_image_admin():
    body=json.loads(request.data)
    owner_type=body['owner_type'] # Store, User, Product
    owner_id=body['owner_id']
    name=body['name']
    img_type=body['img_type']
    url=body['url']
    position=body['position']

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    if not body or "user_id" not in body:
        return jsonify({"msg":f"Es necesario definir el user_id que sera propietario de la imagen que se creara", "ok":False}),400

    
    user_id=body['user_id']
    
    # Validar tipo de entidad
    valid_types = ['store', 'product', 'user', 'menu']
    if owner_type not in valid_types:
        return jsonify({"msg":f"Tipo no válido. Debe ser uno de: {valid_types}","ok":False }),400
    
    
    # Validar que el objeto exista antes de asignarlo
    model_map = {
        'store': Store,
        'product': Product,
        'user': User,
        'menu': Menu
    }
    # Validar que el objeto relacionado exista antes de asignarlo
    entity_model = model_map.get(owner_type)
    if not db.session.get(entity_model, owner_id):
        return jsonify({"msg":f"{owner_type.capitalize()} con ID {owner_id} no existe.","ok":False}),400

    
    # solo aceptamos una imagen index
    if img_type == 'index':
        existing_index = Image.query.filter_by(owner_type=owner_type,owner_id=owner_id,type='index').first()
        if existing_index:
            return jsonify({"msg":f"Ya existe una imagen de tipo 'index' para {owner_type} con ID {owner_id}.","ok":False}),400

    # Crear imagen
    image = Image(
        owner_type=owner_type,
        owner_id=owner_id,
        name=name,
        type=img_type,
        url=url,
        position=position,
        user_id=user_id
    )

    db.session.add(image)
    db.session.commit()
    # Aramamos la respuesta
    response=jsonify({
        "msg": "Imagen creada con éxito",
        "ok": True,
        "data": image.serialize()
    })
    return response,200




# Endpoint de creacion de Imagen
@routes_image.route('/create', methods=['POST'])
@jwt_required()
def add_image():
    body=json.loads(request.data)
    owner_type=body['owner_type'] # Store, User, Product, Menu
    owner_id=body['owner_id']
    name=body['name']
    img_type=body['img_type']
    url=body['url']
    position=body['position']

    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Validar tipo de entidad
    valid_types = ['store', 'product', 'user', 'menu']
    if owner_type not in valid_types:
        return jsonify({"msg":f"Tipo no válido. Debe ser uno de: {valid_types}","ok":False}),400
    

    # Validar que el objeto exista antes de asignarlo
    model_map = {
        'store': Store,
        'product': Product,
        'user': User,
        'menu': Menu
    }
    # Validar que el objeto relacionado exista antes de asignarlo
    entity_model = model_map.get(owner_type)
    target_enity=db.session.get(entity_model, owner_id)
    if not target_enity:
        return jsonify({"msg":f"{owner_type.capitalize()} con ID {owner_id} no existe.","ok":False}),400
    
    # solo aceptamos una imagen index
    if img_type == 'index':
        existing_index = Image.query.filter_by(owner_type=owner_type,owner_id=owner_id,type='index').first()
        if existing_index:
            return jsonify({"msg":f"Ya existe una imagen de tipo 'index' para {owner_type} con ID {owner_id}.","ok":False}),400

    # Crear imagen
    image = Image(
        owner_type=owner_type,
        owner_id=owner_id,
        name=name,
        type=img_type,
        url=url,
        position=position,
        user_id=user.id
    )

    db.session.add(image)
    db.session.commit()

    # Aramamos la respuesta
    response=jsonify({
        "msg": "Imagen creada con éxito",
        "ok": True,
        "data": image.serialize()
    })
    return response,200






# Image Get 
@routes_image.route("/<string:entity_type>/<int:entity_id>", methods=["GET"])
@jwt_required()
def get_images_for(entity_type: str, entity_id: int):
    image=Image.query.filter_by(owner_type=entity_type, owner_id=entity_id).all()
    if image:
        return jsonify(image.serialize())

# Image Delete 
@routes_image.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_image_for(id: int):
    image_exists=Image.query.filter_by(id=id).first()
    if not image_exists:
            return jsonify({"msg":f"No existe una imagen con ID {id}.","ok":False}) , 400
    
    db.session.delete(image_exists)
    db.session.commit()
    return jsonify({"msg":"Imagen eliminada con exito","ok":True}),200

    


