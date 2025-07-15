
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User, Store,Image,Product,UserPoint,Menu,Category
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
import json,yaml


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
    current_user_id = get_jwt_identity()
    #user = User.query.get(current_user_id)
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


@routes_store.route('/admin/list', methods=['GET'])
@jwt_required()
def stores_list():
    stores = Store.query.all()
    # Aramamos la respuesta
    response=jsonify({
        "msg": "Listado de Stores",
        "ok": True,
        "data": [store.serialize() for store in stores]
    })
    return response,200
    return jsonify([store.serialize() for store in stores]), 200
