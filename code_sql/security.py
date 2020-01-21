# -*- coding: utf-8 -*-
from werkzeug.security import safe_str_cmp # importa la funcion para compara strings 
from user import User


def authenticate(username, password):
    user = User.findByUser(username)
    if user and safe_str_cmp(user.password, password):
        return user
    
def identity(payload):
    user_id = payload['identity']
    return User.findById(user_id)