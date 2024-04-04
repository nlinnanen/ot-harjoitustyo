from entities.member import Member
from entities.user import User
from db import create_db_conn, member_repository, user_repository
from db.user_repository import UserRepository
from db.member_repository import MemberRepository

class InvalidCredentialsError(Exception):
    pass


def admin_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.user.admin:
            raise PermissionError("Only admins can perform this operation")
        return func(self, *args, **kwargs)
    return wrapper
        

class RegistryService():
    def __init__(self, conn = create_db_conn()):
        self.user_repository = UserRepository(conn)
        self.member_repository = MemberRepository(conn)
        self.user = None

    def log_in(self, email, password):
        user = self.user_repository.get_user_by_email(email)
        if not user or user.password != password:
            raise InvalidCredentialsError()
        
        self.user = user
        return user

    def log_out(self):
        self.user = None
    
    def get_current_user(self):
        return self.user

    @admin_required
    def delete_member(self, member_id):
        self.member_repository.delete_member(member_id)

    @admin_required
    def add_user_and_member(self, **kwargs):
        user_id = self.user_repository.add_user(**kwargs)
        self.member_repository.add_member(user_id=user_id, **kwargs)
    
    @admin_required
    def update_member(self, member_id, **kwargs):
        for field in Member.__annotations__:
            if field not in kwargs and field not in ['id', 'created_at']:
                raise ValueError(f"Missing required field: {field}")
        self.member_repository.update_member(member_id, **kwargs)

    