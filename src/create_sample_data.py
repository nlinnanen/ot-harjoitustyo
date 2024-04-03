

from faker import Faker

from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository
from repositories import member_repository
from repositories import user_repository

fake = Faker(locale='fi_FI')


def create_sample_user(user_repository: UserRepository):
    return user_repository.add_user(
        email=fake.email(),
        password="password"
    )


def create_sample_member(member_repository: MemberRepository, user_id: str):
    member_repository.add_member(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        start_year=fake.year(),
        member_until=fake.date_between(start_date='-5y', end_date='+1y').isoformat(),
        home_municipality=fake.city(),
        user_id=user_id
    )


def create_sample_data(user_repository: UserRepository, member_repository: MemberRepository):
    user_id = create_sample_user(user_repository)
    create_sample_member(member_repository, user_id)


if __name__ == "__main__":
    for _ in range(10):
        create_sample_data(user_repository, member_repository)
