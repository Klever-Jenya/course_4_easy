from flask_restx import Resource, Namespace

from requireds import auth_required
from dao.models.genre import Genre, GenreSchema
from implemented import genre_service
from setup import db

genre_ns = Namespace('genres')


@genre_ns.route('/')  # работает
class GenresView(Resource):
    # @auth_required
    def get(self):
        all_genres = genre_service.get_all()
        res = GenreSchema(many=True).dump(all_genres)
        return res, 200


@genre_ns.route('/<int:rid>')  # (работает)
class GenreView(Resource):
    # @auth_required
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200
