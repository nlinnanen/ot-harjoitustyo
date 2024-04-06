

import unittest
from db.utils import NotFoundError
from entities.user import User
from db import create_db_conn, delete_db_contents
from db.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.db_conn = create_db_conn("5433")
        delete_db_contents(self.db_conn)
        self.user_repository = UserRepository(self.db_conn)
        new_user_admin = User("admin@admin.com", "admin", True)
        new_user_normal = User("normal@normal.com", "normal", False)
        self.user_admin = self.user_repository.add_user(new_user_admin)
        self.user_normal = self.user_repository.add_user(new_user_normal)

    def test_add_user(self):
        print("Testing add user")
        user_admin = User("admin@admin.com", "admin", True)
        delete_db_contents(self.db_conn)
        self.user_repository.add_user(user_admin)
        users = self.user_repository.get_all_users()
        self.assertEqual(sum(1 for _ in users), 1)

    def test_get_all_users(self):
        users = self.user_repository.get_all_users()
        self.assertEqual(sum(1 for _ in users), 2)

    def test_get_user_by_id(self):
        user = self.user_repository.get_user_by_id(self.user_admin.id)
        self.assertEqual(user.email, "admin@admin.com")
        self.assertEqual(user.password, "admin")

    def test_get_user_by_id_fail(self):
        with self.assertRaises(NotFoundError):
            self.user_repository.get_user_by_id(-1)

    def test_get_user_by_email(self):
        user = self.user_repository.get_user_by_email("admin@admin.com")
        self.assertEqual(user.id, self.user_admin.id)

    def test_get_user_by_email_fail(self):
        with self.assertRaises(NotFoundError):
            self.user_repository.get_user_by_email("ei@loydy.com")

    def test_update_user(self):
        user = self.user_repository.get_user_by_id(self.user_admin.id)
        user.email = "admin@example.com"
        self.user_repository.update_user(user)
        user = self.user_repository.get_user_by_id(self.user_admin.id)
        self.assertEqual(user.email, "admin@example.com")

    def test_update_user_fail_without_id(self):
        user = User(
            email="fail@fail.com",
            password="fail",
            admin=False
        )
        with self.assertRaises(ValueError):
            self.user_repository.update_user(user)

    def test_update_user_fail(self):
        self.user_admin.id = -1
        with self.assertRaises(NotFoundError):
            self.user_repository.update_user(self.user_admin)

    def test_delete_user(self):
        self.user_repository.delete_user(self.user_normal.id)
        users = self.user_repository.get_all_users()
        self.assertEqual(sum(1 for _ in users), 1)

    def test_delete_user_fail(self):
        with self.assertRaises(NotFoundError):
            self.user_repository.delete_user(-1)

    def tearDown(self):
        delete_db_contents(self.db_conn)
        self.db_conn.close()
