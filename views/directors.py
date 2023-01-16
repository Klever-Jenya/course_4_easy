from flask import request
from flask_restx import Resource, Namespace

from dao.models.director import Director, DirectorSchema
from requireds import auth_required

from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self, filters):
        rs = db.session.query(Director).all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

