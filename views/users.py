from flask import request
from flask_restx import Resource, Namespace
from dao.models.user import UserSchema, User
from implemented import user_service
from setup import db

user_ns = Namespace('user')


@user_ns.route('/<int:uid>')
class UsersView(Resource):
    # - **GET** /user/ — получить информацию о пользователе (его профиль)
    def get(self, uid: int):  # (работает)
        try:
            user_by_id = db.session.query(User).get(uid)
            user = UserSchema().dump(user_by_id)
            return user, 200
        except Exception as e:
            return str(e), 404

    # - **PATCH** /user/ — изменить информацию пользователя (имя, фамилия, любимый жанр).
    def patch(self, uid):  # (работает)
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid

        user_service.update(req_json)  # services.user.UserService.
        return "", 204


@user_ns.route("/password")
class UpdateUserPasswordViews(Resource):
    # - **PUT** /user/password — обновить пароль пользователя,
    # для этого нужно отправить два пароля *password_1* и *password_2.*
    def put(self):  # (работает)
        req_json = request.json

        email = req_json.get("email")
        old_password = req_json.get("old_password")
        new_password = req_json.get("new_password")

        user = user_service.get_user_by_email(email)

        # user.password - хешированный пароль, old_password - не хешированный пароль
        if user_service.compare_passwords(
                user.password, old_password):
            user.password = user_service.make_user_password_hash(new_password)
            result = UserSchema().dump(user)
            user_service.update(result)
            print("пароль обновлен")
        else:
            print("пароль не обновлен")

        return "", 201
