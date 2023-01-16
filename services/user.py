import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_user_by_email(self, email):
        return self.dao.get_user_by_email(email)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.make_user_password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    # def get_hash(password):
    #     return hashlib.md5(password.encode('utf-8')).hexdigest()

    def make_user_password_hash(self, password):
        return base64.b64decode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    # сравнивает хешированный пароль с нехишерованным  для аутентификации
    def compare_passwords(self, password_hash, password) -> bool:

        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)