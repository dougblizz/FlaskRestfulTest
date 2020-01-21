# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:16:34 2019

@author: NB-DOCANDO
"""

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, Items

app = Flask(__name__)
app.secret_key = 'Jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth


    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
if __name__ == '__main__':
    app.run(port = 5000, debug = True)

