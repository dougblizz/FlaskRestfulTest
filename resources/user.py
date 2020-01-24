# -*- coding: utf-8 -*-
#import sqlite3 #Sin SQLAlchemy
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import  (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from blacklist import BLACKLIST
from models.user import UserModel

#Inicializa el objeto
_user_parser = reqparse.RequestParser() 
#Aqui definimos el formato del Json
_user_parser.add_argument('username', 
                       type = str, 
                       required = True, 
                       help = 'El usuario no puede ir en blanco'
                       )
        
_user_parser.add_argument('password', 
                       type = str, 
                       required = True, 
                       help = 'El password no puede ir en blanco'
                       )

class UserRegister(Resource):    
    
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.findByUser(data['username']):
            return {'message': 'el usuario ya existe'}, 400
        
        #Como el diccionaro viene en orden, lo podemos comprimir usando **data
        user = UserModel(**data)
        
        user.save_to_db()
        
        #Sin SQLAlchemy
        '''
        connection = sqlite3.connect("MyDB.db")

        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"],))
        
        connection.commit()
        connection.close
        '''
        
        return {"message": "Usuario creado con exito"}, 201
    
class User(Resource):
    
    @classmethod
    def get(cls, user_id):
        user = UserModel.findById(user_id)
        if user:
            return user.json()
        else:
            return {'message': 'el usuario no existe'}, 404
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.findById(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'el usuario fue borrado'}, 200
        else:
            return {'message': 'el usuario no existe'}, 404
        
class UserLogin(Resource):
    
    parser = reqparse.RequestParser() #Inicializa el objeto
    #Aqui definimos el formato del Json
    parser.add_argument('username', 
                       type = str, 
                       required = True, 
                       help = 'El usuario no puede ir en blanco'
    )
        
    parser.add_argument('password', 
                       type = str, 
                       required = True, 
                       help = 'El password no puede ir en blanco'
    )
    
    @classmethod
    def post(cls):
        #tomar data del parser
        data = _user_parser.parse_args()
        
        #encontrar usario en la base de datos
        user = UserModel.findByUser(data['username'])
        
        #Revisar password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity = user.id, fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'credenciales incorrectas'}, 401
    
class TokenRefresh(Resource):
    
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh = False)
        return {'access_token': new_token}, 200
    
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti es "jwt ID", su identificador
        BLACKLIST.add(jti)
        return {'message': 'termino sesion exitosamente'}, 200
    
    