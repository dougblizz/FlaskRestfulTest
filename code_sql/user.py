# -*- coding: utf-8 -*-
import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
        
    @classmethod        
    def findByUser(cls, username):
        connection = sqlite3.connect("MyDB.db")
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        
        if row:
            user  = cls(*row)# *row es lo mismo que = "row[0]. row[1], row[2]"
        else:
            user = None
        connection.close()
        return user
    
    @classmethod        
    def findById(cls, _id):
        connection = sqlite3.connect("MyDB.db")
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        
        if row:
            user  = cls(*row)# *row es lo mismo que = "row[0]. row[1], row[2]"
        else:
            user = None
        connection.close()
        return user

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
        
        if User.findByUser(data['username']):
            return {'message': 'el usuario ya existe'}, 400
        
        connection = sqlite3.connect("MyDB.db")

        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"],))
        
        connection.commit()
        connection.close
        return {"message": "Usuario creado con exito"}, 201