

import unittest

from db import create_db_conn, delete_db_contents
from db.member_repository import MemberRepository
from db.user_repository import UserRepository
from db.utils import NotFoundError
from entities.user import User
from services.registry_service import RegistryService


class RegistryServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        connection = create_db_conn("5433")
        self.registry = RegistryService(
            UserRepository(connection),
            MemberRepository(connection)
        )
        delete_db_contents(connection)
        user = self.registry.user_repository.add_user(
            User(email="admin@admin.com", password="admin", admin=True))
        self.registry.log_in(user.email, user.password)
        self.member1 = self.registry.add_member(
            first_name="Teemu",
            last_name="Teekkari",
            start_year=2020,
            member_until="2025-12-31",
            home_municipality="Helsinki",
            user_id=user.id
        )
        self.user2 = self.registry.add_user("example@example.com", "example")
        self.member2 = self.registry.add_member(
            first_name="example",
            last_name="example",
            start_year=2020,
            member_until="2025-12-31",
            home_municipality="example",
            user_id=self.user2.id
        )

    def test_get_all_members(self):
        members = self.registry.get_all_members()
        self.assertEqual(sum(1 for _ in members), 2)

    def test_get_member_by_id(self):
        member = self.registry.get_member_by_id(
            self.member2.id)  # type: ignore
        self.assertEqual(member.get_full_name(), "example example")

    def test_get_member_by_id_fail(self):
        with self.assertRaises(NotFoundError):
            self.registry.get_member_by_id(-1)

    def test_delete_member(self):
        if self.member2.id is None:
            return self.fail("Member2 id is None")
        self.registry.delete_member(self.member2.id)
        members = self.registry.get_all_members()
        self.assertEqual(sum(1 for _ in members), 1)

    def test_delete_member_fail(self):
        with self.assertRaises(NotFoundError):
            self.registry.delete_member(-1)

    def test_update_member(self):
        if self.member1.id is None:
            return self.fail("Member1 id is None")
        self.member1.home_municipality = "Vantaa"
        self.registry.update_member(
            member_id=self.member1.id,
            home_municipality="Vantaa"
        )
        member = self.registry.get_member_by_id(self.member1.id)
        self.assertEqual(member.home_municipality, "Vantaa")
    
    def test_update_self(self):
        if self.member1.id is None:
            return self.fail("Member1 id is None")
        self.registry.update_current_member(
            home_municipality="Vantaa"
        )
        member = self.registry.get_member_by_id(self.member1.id)
        self.assertEqual(member.home_municipality, "Vantaa")

    def test_admin_required(self):
        with self.assertRaises(PermissionError):
            self.registry.log_in(self.user2.email, self.user2.password)
            self.registry.add_member(
                first_name="Matti",
                last_name="Meikäläinen",
                start_year=2020,
                member_until="2025-12-31",
                home_municipality="Vantaa"
            )

    def test_add_member(self):
        member = self.registry.add_member(
            first_name="Matti",
            last_name="Meikäläinen",
            start_year=2020,
            member_until="2025-12-31",
            home_municipality="Vantaa"
        )
        self.assertEqual(member.get_full_name(), "Matti Meikäläinen")
        members = self.registry.get_all_members()
        self.assertEqual(sum(1 for _ in members), 3)
