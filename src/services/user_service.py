
from repositories import user_repository
from repositories.user_repository import UserRepository


class UserService():
    def __init__(self):
        self.user_repository = user_repository

    def log_in(self, email, password):
        user = self.user_repository.get_user_by_email(email)
        if user and user[2] == password:
            return user
        return None