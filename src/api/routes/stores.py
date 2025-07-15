
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User, Store,Image,Product,UserPoint,Menu,Category
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
import json,yaml
from api.constants import ROLE_ADMIN,ROLE_USER, ROLE_STORE

routes_store = Blueprint('stores', __name__,url_prefix='/api/store')

# Allow CORS requests to this API
CORS(routes_store)


## STORES ##
# Endpoint de creacion de tienda
@routes_store.route('/create', methods=['POST'])
@jwt_required()
def store_create():
    body=json.loads(request.data)
    if body is None or len(body['nombre']) < 1 or len(body['direccion']) < 1 :
        return jsonify({"msg": "Los datos enviados no son suficientes"}), 400
    if Store.query.filter((Store.nombre == body['nombre']) | (Store.direccion == body['direccion'])).first():
        return jsonify({"msg": "No es posible crear una tienda con esos datos"}), 409
    
    # Access the identity of the current user with get_jwt_identity    
    current_user_id = get_jwt_identity()

    local_store= Store()
    local_store.nombre=body['nombre']
    local_store.user_id=current_user_id
    local_store.direccion=body['direccion']

    db.session.add(local_store)
    db.session.commit()

    # Aramamos la respuesta
    response=jsonify({
        "msg": "Store creado con exito",
        "ok": True,
        "data": local_store.serialize()
    })
    return response,200

@routes_store.route('/list', methods=['GET'])
@jwt_required()
def stores_list():
    # Access the identity of the current user with get_jwt_identity    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    #Se valida el Rol (no seria necesario) y que este activo
    valid_types = [ ROLE_USER, ROLE_STORE,ROLE_ADMIN]
    if user.role not in valid_types or not user.is_active:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    stores = Store.query.filter_by(is_active=True, user_id=user.id).all()
    # Aramamos la respuesta
    response=jsonify({
        "msg": f"Listado de Stores de {user.username}", 
        "ok": True,
        "data": [store.serialize() for store in stores]
    })
    return response,200

@routes_store.route('/admin/list', methods=['GET'])
@jwt_required()
def stores_list_admin():
    # Access the identity of the current user with get_jwt_identity    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    stores = Store.query.all()
    # Aramamos la respuesta
    response=jsonify({
        "msg": "Listado de Stores",
        "ok": True,
        "data": [store.serialize() for store in stores]
    })
    return response,200
    return jsonify([store.serialize() for store in stores]), 200




# Store Delete 
# La tienda debe ser desactivada para poder borrarla
@routes_store.route("/admin/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_store_for(id: int):
    # Access the identity of the current user with get_jwt_identity    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    image_exists=Image.query.filter_by(id=id,is_active=False).first()
    if not image_exists:
            return jsonify({"msg":f"No existe una Tienda inactiva con ID {id}","ok":False}) , 400
    
    db.session.delete(image_exists)
    db.session.commit()
    return jsonify({"msg":"Tienda eliminada con exito","ok":True}),200


# Store Disable
@routes_store.route("/admin/<int:id>/deactivate", methods=["PATCH"])
@jwt_required()
def deactivate_store_for(id: int):

    # Access the identity of the current user with get_jwt_identity    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    

    store_exists=Image.query.filter_by(id=id,is_active=True).first()
    if not store_exists:
            return jsonify({"msg":f"No existe una tienda con ID {id}.","ok":False}) , 400
    
    store_exists.is_active=False
    db.session.add(store_exists)
    db.session.commit()

    # Aramamos la respuesta
    response=jsonify({
        "msg": f"Tienda {store_exists.nombre} deshabilitada con exito",
        "ok": True,
        "data": store.serialize()
    })
    return response,200
