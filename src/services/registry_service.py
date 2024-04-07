from typing import Generator, Optional
from entities.member import Member
from entities.user import User
from db import user_repository as default_user_repository
from db import member_repository as default_member_repository


class InvalidCredentialsError(Exception):
    pass


def admin_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.user or not self.user.admin:
            raise PermissionError("Only admins can perform this operation")
        return func(self, *args, **kwargs)
    return wrapper

def user_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.user:
            raise PermissionError("You must be logged in to perform this operation")
        return func(self, *args, **kwargs)
    return wrapper

class RegistryService():
    def __init__(self,
                 user_repository=default_user_repository,
                 member_repository=default_member_repository
                 ):
        self.user_repository = user_repository
        self.member_repository = member_repository
        self.user: Optional[User] = None

    def log_in(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(email)
        if not user or user.password != password:
            raise InvalidCredentialsError()

        self.user = user
        return user

    @user_required
    def log_out(self):
        self.user = None

    @user_required
    def get_current_user(self):
        return self.user

    @user_required
    def get_all_members(self) -> "Generator[Member, None, None]":
        return self.member_repository.get_all_members()

    @user_required
    def get_member_by_id(self, member_id: int) -> Member:
        return self.member_repository.get_member_by_id(member_id)

    @user_required
    def update_current_member(self, **kwargs):
        if not self.user:
            raise PermissionError("You must be logged in to perform this operation")
        current_member = self.member_repository.get_member_by_user_id(self.user.id)
        self.member_repository.update_member(Member(**{**current_member.__dict__, **kwargs}))

    @admin_required
    def add_member(self, **kwargs):
        return self.member_repository.add_member(Member(**kwargs))

    @admin_required
    def delete_member(self, member_id: int):
        self.member_repository.delete_member(member_id)

    @admin_required
    def add_user(self, email: str, password: str, admin: bool = False):
        return self.user_repository.add_user(User(email=email, password=password, admin=admin))

    @admin_required
    def update_member(self, member_id, **kwargs):
        member = self.member_repository.get_member_by_id(member_id)
        # The dictionary is created and then unpacked to ensure that the keys are unique
        self.member_repository.update_member(Member(**{**member.__dict__, **kwargs}))
