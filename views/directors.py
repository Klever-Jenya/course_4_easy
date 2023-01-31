from flask import request
from flask_restx import Resource, Namespace

from dao.models.director import Director, DirectorSchema
from requireds import auth_required

from setup import db

director_ns = Namespace('directors')


@director_ns.route('/')  # работает
class DirectorsView(Resource):
    # @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:rid>')  # (работает)
class DirectorView(Resource):
    # @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

