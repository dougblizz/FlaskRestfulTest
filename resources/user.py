# -*- coding: utf-8 -*-
#import sqlite3 #Sin SQLAlchemy
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
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
    
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
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