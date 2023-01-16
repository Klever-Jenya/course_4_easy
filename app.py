# основной файл приложения. здесь конфигурируется
# фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение
import hashlib

# Пример

from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.auths import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app(Config())
app.debug = True

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=10001, debug=True)
