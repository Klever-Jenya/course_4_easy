from flask import request
from flask_restx import Resource, Namespace

from dao.models.movie import Movie, MovieSchema
from implemented import movie_service
from requireds import auth_required
from setup import db

movie_ns = Namespace('movies')


# авторизация - предоставление лицу или группе лиц
# прав на выполнение определенных действий

# Для того чтобы все ссылки корректно работали, их нужно обернуть в декоратор,
# в котором мы будем проверять переданный токен.

@movie_ns.route('/')  # (работает без фильтров)
class MoviesView(Resource):
    # @auth_required
    def get(self):
        status = request.args.get("status")  # (работает) новинки new.
        page = request.args.get("page")  # (не работает) точно число

        filters = {
            "status": status,
            "page": page
        }

        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200


@movie_ns.route('/<int:bid>')  # (работает)
class MovieView(Resource):
    @auth_required
    def get(self, bid):
        movie_id = db.session.query(Movie).get(bid)
        movie = MovieSchema().dump(movie_id)
        return movie, 200
