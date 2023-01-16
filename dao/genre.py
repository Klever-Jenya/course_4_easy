from config import Config
from dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Genre).get(bid)

        # пагинировать-разбить на страницы

    def get_all(self, filters):
        page = filters.get("page")

        if page is not None:  # пагинацию нельзя в сервисах
            result = self.session.query(Genre). \
                paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE, error_out=False).items
            return result

        return self.session.query(Genre).all()
