from flask import request

from config import Config
from dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):  # (работает)
        return self.session.query(Director).get(bid)

    def get_all(self):
        page = request.args.get("page")

        # (не работает)--------------------------
        if page is not None:  # пагинацию нельзя в сервисах
            result = self.session.query(Director). \
                paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE, error_out=False).items
            return result

        return self.session.query(Director).all()  # (работает)

