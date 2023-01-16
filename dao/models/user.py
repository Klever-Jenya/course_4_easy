import hashlib

from marshmallow import Schema, fields

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # null-обязательно # по нему будет осуществлен доступ на сайт (*уникальное*)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # не забывайте, что пароль тут будет в хешированном виде ????---
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()  # (load_only=True)-загружается но не выводиться, пока оставляем для проверки
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()


