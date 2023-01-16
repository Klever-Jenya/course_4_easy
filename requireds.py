import jwt
from flask import request
from flask_restx import abort

from constants import SECRET, ALGO


# авторизация - предоставление лицу или группе лиц
# прав на выполнение определенных действий
def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])
        except Exception as e:
            print("JWT Decode Error", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


# функции админа
def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, SECRET, algorithms=[ALGO])
            role = user.get("role")
            if role != "admin":
                abort(403)

        except Exception as e:
            print("JWT Decode Error", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
