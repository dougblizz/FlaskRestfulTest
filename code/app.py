# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:16:34 2019

@author: NB-DOCANDO
"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

items = []

class Item(Resource):
    parse = reqparse.RequestParser() #Inicializa el objeto
    #Aqui definimos el formato del Json
    parse.add_argument('price', 
                       type = float, 
                       required = True, 
                       help = 'El precio no puede ir en blanco'
    )
    @jwt_required()
    def get(self, name):
        # Despues de la "," dentro de la funcion lambda estamos accediendo a los items
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
        # aux = [x for x in items if x['name'] == name ]
        # if (len(aux) != 0):
        #     return aux
        # else:
        #     return {"item": None}, 404
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"el {name} ya existe"}, 400
        else:
            data = Item.parse.parse_args()
            item = {"name": name, "price": data['price']}
            items.append(item)
            return item, 201
        
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'El item fue eliminado'}, 200
    
    def put(self, name):
        #aqui revisa el json con el parse que configuramos
        data = Item.parse.parse_args()
        
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
            return item, 201
        else:
            item.update(data)
            return item, 200
        
    
class Items(Resource):
    def get(self):
        return {'items': items}, 200
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port = 5000, debug = True)


itemsX = [{"name": "dpug", "price": 45.4}, {"name": "rafa", "price": 6}]
# name= "duada"

# aux = [x for x in items if x['name'] == name ]
# print