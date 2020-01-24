# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 11:34:49 2019

@author: NB-DOCANDO
"""

#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() #Inicializa el objeto
    #Aqui definimos el formato del Json
    parser.add_argument('price', 
                       type = float, 
                       required = True, 
                       help = 'El precio no puede ir en blanco'
    )
    
    parser.add_argument('store_id', 
                       type = int, 
                       required = True, 
                       help = 'Cada item tiene que tener un store id.'
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)
        
        if item:
            return item.json(), 200
        return {'item': None}, 404
        
    
    def post(self, name):
        if ItemModel.findByName(name):
            return {"message": f"el {name} ya existe"}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, data['price'], data['store_id'])
            
            try: 
                #item.insert() sin SQLAlchemy
                item.save_to_db()
            except:
                return {"message": "ERROR al insertar el dato"}, 500 #internal server error
            
            return item.json(), 201
        
        
    def delete(self, name):
        item = ItemModel.findByName(name)
        
        if item:
            item.delete_from_db()
        return {'message': 'El item fue eliminado'}, 200   
        
        #Sin SQLAlchemy
        '''
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        
        return {'message': 'El item fue eliminado'}, 200
        '''
    
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.findByName(name)
        
        if item is None:
            item  = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            
        item.save_to_db()
            
        return  item.json()
        
        #Sin SQLAlchemy
        '''
        #aqui revisa el json con el parse que configuramos
        data = Item.parser.parse_args()
        
        item = ItemModel.findByName(name)
        update_item = ItemModel(name, data["price"])
        
        if item is None:
            try:
                update_item.insert()
            except:
                {'message': 'Error al insertar el item'}, 500
            return update_item.json(), 201
        else:
            try:
                update_item.update()
            except:
                {'message': 'Error al actualizar el item'}, 500
            return update_item.json(), 200
        '''
    

        
        
    
class Items(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.findAll()))}
        #Con compresion [item.json() for item in ItemModel.query.all()]
        
        #Sin SQLAlchemy
        '''
        connection = sqlite3.connect('MyDB.db')
        cursor = connection.cursor()
            
        query = "SELECT * FROM items"
        result = cursor.execute(query)
                       
        items = []
        
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.close() 
        
        return {'items': items}
        '''