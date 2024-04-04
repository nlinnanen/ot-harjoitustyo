
from entities.member import Member
from entities.user import User
from repositories import member_repository, user_repository
from repositories.user_repository import UserRepository

class InvalidCredentialsError(Exception):
    pass


def admin_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.user.admin:
            raise PermissionError("Only admins can perform this operation")
        return func(self, *args, **kwargs)
    return wrapper
        

class RegistryService():
    def __init__(self):
        self.user_repository = user_repository
        self.member_repository = member_repository
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
    def add_member(self, kwargs):
        for field in Member.__annotations__:
            if field not in kwargs and field not in ['id', 'created_at']:
                raise ValueError(f"Missing required field: {field}")
        return self.member_repository.add_member(**kwargs)
    
    @admin_required
    def update_member(self, member_id, **kwargs):
        for field in Member.__annotations__:
            if field not in kwargs and field not in ['id', 'created_at']:
                raise ValueError(f"Missing required field: {field}")
        self.member_repository.update_member(member_id, **kwargs)

    