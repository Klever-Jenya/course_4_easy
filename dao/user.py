from dao.models.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.name == username).one_or_none()

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()  # one_or_none - вернуть один или нон

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        # user.name = user_d.get("name")
        # user.surname = user_d.get("surname")
        # user.favorite_genre = user_d.get("favorite_genre")
        # user.password = user_d.get("password")  # - а также в случае необходимости сменить пароль.
        for k, v in user_d.items():
            setattr(user, k, v)  # setattr - установить атрибут по ключу
            # объект: User, ключ: name,surname..., значение: Вася,  Пупкин ...

        self.session.add(user)
        self.session.commit()

    # добавить фильм в закладки, чтобы просмотреть позже
    # -------------???-----------
    def add_to_bookmarks(self, movie):  # создать в базе данных столбец??
        self.movie = movie
        bookmarks = []
        bookmarks.append(self.movie)
        return bookmarks  # просмотр сохраненных закладок


