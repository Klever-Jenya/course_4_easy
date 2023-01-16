from config import Config
from dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Movie).get(bid)

    # пагинировать-разбить на страницы
    def get_all(self, filters):
        status = filters.get("status")
        page = filters.get("page")

        if status == "new" and page is not None:  # cортировка и пагинация
            result = self.session.query(Movie).order_by(Movie.year.desc()) \
                .paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE,
                          error_out=False).items  # items (для пагинации)
            # error_out=False - если пагинация с ошибкой, то будет выводиться без пагинации (по умолчанию True)
            return result

        elif status == "new":  # просто сортировка
            result = self.session.query(Movie).order_by(Movie.year.desc()).all()
            # all- не работает с пагинацией (для не пагинации)
            return result

        elif page is not None:  # пагинацию нельзя в сервисах
            result = self.session.query(Movie). \
                paginate(int(page), Config.ITEMS_PER_PAGE, max_per_page=Config.MAX_PAGE, error_out=False).items
            return result

        return self.session.query(Movie).all()  # если нет ничего-выводим как есть
