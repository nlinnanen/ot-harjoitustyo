

import datetime
import sys
import unittest
from db import create_db_conn, delete_db_contents
from db.member_repository import MemberRepository
from db.user_repository import UserRepository
from db.utils import NotFoundError
from entities.member import Member
from entities.user import User


class MemberRepositoryTest(unittest.TestCase):
    def setUp(self):
        conn = create_db_conn("5433")
        self.member_repository = MemberRepository(conn)
        self.user_repository = UserRepository(conn)
        delete_db_contents(conn)
        _user1 = User(
            email="user@user.com",
            password="password",
        )
        self.user1 = self.user_repository.add_user(_user1)
        _member1 = Member(
            first_name="Teemu",
            last_name="Teekkari",
            start_year=2020,
            member_until=datetime.date(2025, 12, 31),
            home_municipality="Helsinki",
            user_id=self.user1.id
        )
        _member2 = Member(
            first_name="Hannu",
            last_name="Humanisti",
            start_year=2020,
            member_until=datetime.date(2020, 12, 31),
            home_municipality="Espoo"
        )
        self.member1 = self.member_repository.add_member(_member1)
        self.member2 = self.member_repository.add_member(_member2)

    def test_add_member(self):
        delete_db_contents(self.member_repository.db_conn)
        member_to_add = Member(
            first_name="Matti",
            last_name="Meikäläinen",
            start_year=2020,
            member_until=datetime.date(2025, 12, 31),
            home_municipality="Vantaa"
        )
        member = self.member_repository.add_member(member_to_add)
        self.assertEqual(member.get_full_name(), "Matti Meikäläinen")
        members = self.member_repository.get_all_members()
        self.assertEqual(sum(1 for _ in members), 1)

    def test_get_all_members(self):
        members = self.member_repository.get_all_members()
        self.assertEqual(sum(1 for _ in members), 2)

    def test_get_member_by_id(self):
        if self.member1.id is None:
            return self.fail("Member1 id is None")
        member = self.member_repository.get_member_by_id(self.member1.id)
        self.assertEqual(member.get_full_name(), "Teemu Teekkari")

    def test_get_member_by_id_fail(self):
        with self.assertRaises(NotFoundError):
            self.member_repository.get_member_by_id(-1)

    def test_update_member(self):
        if self.member1.id is None:
            return self.fail("Member1 id is None")

        self.member1.home_municipality = "Vantaa"
        self.member_repository.update_member(self.member1)
        member = self.member_repository.get_member_by_id(self.member1.id)
        self.assertEqual(member.home_municipality, "Vantaa")

    def test_update_member_fail(self):
        with self.assertRaises(NotFoundError):
            fake_member = Member(
                id=-1,
                first_name="Fake",
                last_name="Member",
                start_year=2020,
                member_until=datetime.date(2025, 12, 31),
                home_municipality="Vantaa"
            )
            self.member_repository.update_member(fake_member)

    def test_delete_member(self):
        if self.member2.id is None:
            return self.fail("Member2 id is None")
        self.member_repository.delete_member(self.member2.id)
        members = self.member_repository.get_all_members()
        self.assertEqual(sum(1 for _ in members), 1)

    def test_delete_member_fail(self):
        with self.assertRaises(NotFoundError):
            self.member_repository.delete_member(-1)

    def tearDown(self):
        delete_db_contents(self.member_repository.db_conn)
        self.member_repository.db_conn.close()
