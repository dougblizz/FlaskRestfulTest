# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:34:49 2019

@author: NB-DOCANDO
"""

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser() #Inicializa el objeto
    #Aqui definimos el formato del Json
    parser.add_argument('price', 
                       type = float, 
                       required = True, 
                       help = 'El precio no puede ir en blanco'
    )
    
    @jwt_required()
    def get(self, name):
        item = self.findByName(name)
        
        if item:
            return item, 200
        return {'item': None}, 404
        
    @classmethod
    def findByName(cls, name):
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item': {'name':row[0], 'price':row[1]}}
    
    def post(self, name):
        if self.findByName(name):
            return {"message": f"el {name} ya existe"}, 400
        else:
            data = self.parser.parse_args()
            item = {"name": name, "price": data['price']}
            
            try: 
                self.insert(item)
            except:
                return {"message": "ERROR al insertar el dato"}, 500 #internal server error
            
            return item, 201
        
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
            
        connection.commit()
        connection.close()
        
    def delete(self, name):
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'El item fue eliminado'}, 200
    
    def put(self, name):
        #aqui revisa el json con el parse que configuramos
        data = Item.parser.parse_args()
        
        item = Item.findByName(name)
        update_item = {"name": name, "price": data["price"]}
        
        if item is None:
            try:
                Item.insert(update_item)
            except:
                {'message': 'Error al insertar el item'}, 500
            return update_item, 201
        else:
            try:
                self.update(update_item)
            except:
                {'message': 'Error al actualizar el item'}, 500
            return update_item, 200
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit()
        connection.close()
        
        
    
class Items(Resource):
    def get(self):
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "SELECT * FROM items"
        result = cursor.execute(query)
                       
        items = []
        
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.close() 
        
        return {'items': items}