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

routes_menu = Blueprint('menus', __name__,url_prefix='/api/menu')

# Allow CORS requests to this API
CORS(routes_menu)

## MENUS ##
# Endpoint de creacion de Menu
@routes_menu.route('/create', methods=['POST'])
@jwt_required()
def add_menu():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role != ROLE_STORE:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    body=json.loads(request.data)
    store_id=body['store_id']
    description=body['description']

    if description and description is None:
        return jsonify({"msg":f"Debe ingresar una descripción.","ok":False}),400


    # Se valida existencia de Store 
    existing_store = Store.query.filter_by(id=store_id,user_id=current_user_id).first()
    if not existing_store:
        return jsonify({"msg":f"No existe la tienda {store_id}.","ok":False}),400
    
     # Se valida existencia de Menu 
    existing_menu = Menu.query.filter_by(description=description,store_id=store_id).first()
    if existing_menu:
        return jsonify({"msg":f"Ya existe el menu para la tienda {store_id}.","ok":False}),400
   
    # Crear menu
    menu = Menu(
        store_id=store_id,
        description=description
    )

    db.session.add(menu)
    db.session.commit()

    # Aramamos la respuesta
    response=jsonify({
        "msg": "Menu creado con éxito",
        "ok": True,
        "data": menu.serialize()
    })
    return response,200

@routes_menu.route('/list', methods=['GET'])
@jwt_required()
def menus_list():
   # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role != ROLE_STORE:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    
    # Se valida existencia de Store 
    existing_store = Store.query.filter_by(user_id=current_user_id).first()
    if not existing_store:
        return jsonify({"msg":f"No existen la tienda para el usuario {current_user_id}.","ok":False}),400

    menus=Menu.query.filter_by(store_id=existing_store.id).all()

    # Aramamos la respuesta
    response=jsonify({
        "msg": f"Listado de Menues para {user.username}",
        "ok": True,
        "data": [menu.serialize() for menu in menus]
    })
    return response,200


## SEGUIR ACA 

## MENUS ## ADMIN ##
# Endpoint ADMIN de listado de Menues
@routes_menu.route('/admin/list', methods=['GET'])
@jwt_required()
def menus_list_admin():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != ROLE_ADMIN:
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    menus = Menu.query.all()
    # Aramamos la respuesta
    response=jsonify({
        "msg": "Listado de Menues",
        "ok": True,
        "data": [menu.serialize() for menu in menus]
    })
    return response,200





# Menu Get 
@routes_menu.route("/<string:entity_type>/<int:entity_id>", methods=["GET"])
@jwt_required()
def get_menus_for(entity_type: str, entity_id: int):
    menu=Menu.query.filter_by(owner_type=entity_type, owner_id=entity_id).all()
    if menu:
        return jsonify(menu.serialize())

# Menu Delete 
@routes_menu.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_menu_for(id: int):
    menu_exists=Menu.query.filter_by(id=id).first()
    if not menu_exists:
            return jsonify({"msg":f"No existe una menu con ID {id}.","ok":False}) , 400
    
    db.session.delete(menu_exists)
    db.session.commit()
    return jsonify({"msg":"Menu eliminada con exito","ok":True}),200

    


