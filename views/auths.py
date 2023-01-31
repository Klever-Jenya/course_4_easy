from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service, auth_service

auth_ns = Namespace('auth')


# регистрация = идентификация - процедура, в результате которой для субъекта идентификации выявляется
# его идентификатор (~паспорт, логин+пароль)
@auth_ns.route('/register')  # (работает) передавая email и пароль, создаем пользователя в системе.
class RegisterViews(Resource):

    def post(self):
        req_json = request.json

        email = req_json.get("email")
        password = req_json.get("password")

        if None in [email, password]:
            return "", 400

        user_service.create(req_json)
        return "", 201


# """аутентификация""" - процедура проверки подлинности, например
# проверка подлинности пользователя путем сравнения
# введенного им пароля с паролем, сохраненным в базе данных

@auth_ns.route('/login')  # post- передаем email и пароль и,
# если пользователь прошел аутентификацию, возвращаем пользователю ответ в виде:
class LoginView(Resource):

    def post(self):  # (работает)
        req_json = request.json

        email = req_json.get("email", None)
        password = req_json.get("password", None)

        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email=email, password=password)

        return tokens, 200

    def put(self):  # принимаем пару токенов и, если они валидны, создаем пару новых.
        req_json = request.json

        access_token = req_json.get("access_token")
        refresh_token = req_json.get("refresh_token")

        validated = auth_service.validate_tokens(access_token, refresh_token)

        if not validated:
            return "Invalid token", 400

        # approve -одобрить подтверждать
        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 201  # -+ (выводит не tokens, а null, 201)---------------------

# На данном этапе нужно обязательно проверить работу механизма аутентификации через Postman
# (или используйте любой другой инструмент)
#
# Теперь сделаем -----коммит----- и приступим к последнему шагу.
