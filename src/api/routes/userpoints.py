"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint,current_app
from api.models import db, User, Store,Image,Product,UserPoint,UserPoint,Category
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
import json,yaml
from api.constants import ROLE_ADMIN,ROLE_USER, ROLE_STORE

routes_userpoint = Blueprint('userpoints', __name__,url_prefix='/api/userpoint')

# Allow CORS requests to this API
CORS(routes_userpoint)


## USERPOINTS ##
# Endpoint de creacion de UserPoint
@routes_userpoint.route('/create', methods=['POST'])
@jwt_required()
def add_userpoint():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Solo Role user
    if user.role != ROLE_USER: 
        return jsonify({"msg": f"Usuario no autorizado | {user.role}","ok": False}),401   
    user_id=user.id
    
    # Consistencia en id de usuario
    if user.id is None or not isinstance(user.id,int):
        return jsonify({"msg":f"No se pudo identificar el usuario","ok":False}),400

    # Datos enviados por api
    data = request.get_json()

    # Minimos requermimientos en la estructura del body del endpoint
    if "store_id" not in data or "description" not in data or "points" not in data:
         return jsonify({"msg": "No se alcanzaron los requerimientos para agregar el puntaje. Debe especificar tienda, descripcion y puntaje.","ok": False}),409
    store_id = data.get("store_id")
    description = data.get("description") # Vendria a ser el review del front minimo 10 caracteres
    points = data.get("points")

    # Validacion de consistencia de descripcion: no vacia y con un minimos 10 caracteres
    if description and description is None and len(description) < 10:
        return jsonify({"msg":f"Debe ingresar una descripción de al menos 10 caracteres.","ok":False}),400

    # Se valida existencia de Store y que este activa
    existing_store = Store.query.filter_by(id=store_id,is_active=True).first()
    if not existing_store:
        return jsonify({"msg":f"No existe la tienda {store_id}.","ok":False}),400
    
     # Se valida existencia de UserPoint del usuario
    existing_userpoint = UserPoint.query.filter_by(store_id=store_id,user_id=user_id).first()
    if existing_userpoint:
        return jsonify({"msg":f"Ya existe una reseña para la tienda {store_id}.","ok":False}),400
    
    # Consistencia de puntaje y validación de rango [1-5]
    if points is None or not isinstance(points,int) or points > 5 or points < 1:
        return jsonify({"msg":f"Rango de puntaje no acepatado [1-5]","ok":False}),400


    # Crear userpoint
    userpoint = UserPoint(
        store_id=store_id,
        description=description,
        points=points,
        user_id=user_id
    )
    db.session.add(userpoint)
    db.session.commit()
    existing_store = Store.query.filter_by(id=store_id,is_active=True).first()
    if existing_store.total_points is not None:
        store_total_points=round(userpoint.total(store_id=store_id, session=db.session))
    else:
        store_total_points=points

    existing_store.total_points=store_total_points
    db.session.add(existing_store)
    db.session.commit()


    
    userpoint_seririalized=userpoint.serialize()
    userpoint_seririalized["total_points"] = store_total_points

    # Aramamos la respuesta
    response=jsonify({
        "msg": "Reseña creada con éxito",
        "ok": True,
        "data": userpoint_seririalized
    })
    return response,200

@routes_userpoint.route('/list/<string:user_type>', methods=['GET'])
@jwt_required()
def userpoints_list(user_type:str):
   # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    

    if user_type and user_type == "user" and user.role != ROLE_USER: 
        return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
    if user_type and user_type == "store" and user.role.capitalize() != ROLE_STORE: 
        return jsonify({"msg": f"Usuario no autorizado {user.role} != {ROLE_STORE}","ok": False}),401     
    # if not existing_store:
    if user_type == "user":
        userpoints=UserPoint.query.filter_by(user_id=user.id).all()
    elif user_type == "store":
        # Se valida existencia de Store 
        existing_store = Store.query.filter_by(user_id=user.id).first()
        if not existing_store:
            return jsonify({"msg":f"No existe la tienda para el usuario con ID {user.id}.","ok":False}) , 400
        userpoints=UserPoint.query.filter_by(store_id=existing_store.id).all()
    else:
        return jsonify({"msg":f"No es posible generar el listado con la informacion proporcionada ","ok":False}),400
        
    # Aramamos la respuesta
    response=jsonify({
        "msg": f"Listado de Puntos de Usuario para {user.username}",
        "ok": True,
        "data": [userpoint.serialize() for userpoint in userpoints]
    })
    return response,200


## SEGUIR ACA  

## USERPOINTS ## ADMIN ##
# Endpoint ADMIN de listado de Puntos de Usuario
# @routes_userpoint.route('/admin/list', methods=['GET'])
# @jwt_required()
# def userpoints_list_admin():
#     # Access the identity of the current user with get_jwt_identity
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)

#     if user.role != ROLE_ADMIN:
#         return jsonify({"msg": "Usuario no autorizado","ok": False}),401
    
#     userpoints = UserPoint.query.all()
#     # Aramamos la respuesta
#     response=jsonify({
#         "msg": "Listado de Puntos de Usuario",
#         "ok": True,
#         "data": [userpoint.serialize() for userpoint in userpoints]
#     })
#     return response,200





# # UserPoint Get 
# @routes_userpoint.route("/<string:entity_type>/<int:entity_id>", methods=["GET"])
# @jwt_required()
# def get_userpoints_for(entity_type: str, entity_id: int):
#     userpoint=UserPoint.query.filter_by(owner_type=entity_type, owner_id=entity_id).all()
#     if userpoint:
#         return jsonify(userpoint.serialize())

# # UserPoint Delete 
# @routes_userpoint.route("/<int:id>", methods=["DELETE"])
# @jwt_required()
# def delete_userpoint_for(id: int):
#     userpoint_exists=UserPoint.query.filter_by(id=id).first()
#     if not userpoint_exists:
#             return jsonify({"msg":f"No existe una userpoint con ID {id}.","ok":False}) , 400
    
#     db.session.delete(userpoint_exists)
#     db.session.commit()
#     return jsonify({"msg":"UserPoint eliminada con exito","ok":True}),200

    


