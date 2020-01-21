# -*- coding: utf-8 -*-
from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.findByName(name)
        if store:
            return store.json()
        return {'message': 'Tienda no encontrada'}, 404
    
    def post(self, name):
        if StoreModel.findByName(name):
            return {'message': f'la tienda {name} ya existe'}
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'error al crear una tienda'}, 500
        
        return store.json(), 201
    
    def delete(self, name):
        store = StoreModel.findByName(name)
        if store:
            store.delete_from_db()
            return {'message': 'La tienda se borro correctamente'}, 200
        return {'message': 'Tienda no encontrada'}, 200
    

class StoreList(Resource):
    
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
    
    
