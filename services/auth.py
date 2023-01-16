import calendar
import datetime

import jwt
from flask import abort

from constants import SECRET, ALGO
from services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_user_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

            data = {
                "email": user.email
            }

            min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            data['exp'] = calendar.timegm(min30.timetuple())
            access_token = jwt.encode(data, SECRET, algorithm=ALGO)

            day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
            data['exp'] = calendar.timegm(day130.timetuple())
            refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return tokens, 201

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token,
                          key=SECRET,
                          algorithms=[ALGO])
        email = data.get("email")

        user = self.user_service.get_user_by_email(email=email)

        if user is None:
            raise Exception()

        return self.generate_tokens(email, user.password, is_refresh=True)

    def validate_tokens(self, access_token, refresh_token):  # завалидили токены
        for token in [access_token, refresh_token]:
            try:
                # проверяем что токен нужного формата и не истек
                jwt.decode(jwt=token, key=SECRET, algorithms=[ALGO])
            except Exception:
                return False

            return True

# если refresh, то мы доверяем этому пользователю и не спрашиваем снова пароль
