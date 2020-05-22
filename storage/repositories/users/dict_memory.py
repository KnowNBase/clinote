from knb.errors import NotFoundError
from knb.models import User


class Repository:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id: str) -> User:
        try:
            return self.users[user_id]
        except KeyError:
            raise NotFoundError("user", user_id)
