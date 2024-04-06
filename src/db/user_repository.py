from typing import Generator
from psycopg2.extensions import connection
from db.member_repository import require_id
from db.utils import NotCreatedError, NotFoundError, map_result_to_entity
from entities.user import User


class UserRepository:
    def __init__(self, db_conn: connection):
        """
        Initialize the repository with a database connection.
        :param db_conn: A database connection object.
        """
        self.db_conn = db_conn

    def get_user_by_id(self, user_id: int):
        """
        Fetch a single user by their user ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if not user_data:
                raise NotFoundError("User not found.")
            return map_result_to_entity(User, user_data, cur)

    def get_user_by_email(self, email: str):
        """
        Fetch a single user by their email.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            if not user_data:
                raise NotFoundError("User not found.")
            return map_result_to_entity(User, user_data, cur)

    def get_all_users(self) -> "Generator[User, None, None]":
        """
        Fetch all users from the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            for user in cur:
                yield map_result_to_entity(User, user, cur)

    def add_user(self, user: User) -> User:
        """
        Add a new user to the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password, admin) VALUES (%s, %s, %s) RETURNING *",
                (user.email, user.password, user.admin)
            )
            self.db_conn.commit()
            added_user = cur.fetchone()
            if not added_user:
                raise NotCreatedError("User could not be created.")
            return map_result_to_entity(User, added_user, cur)

    @require_id
    def update_user(self, user: User):
        """
        Update user details based on provided keyword arguments.
        """
        set_clause = ', '.join([f"{key} = %s" for key in user.__dict__])
        values = list(user.__dict__.values())
        values.append(user.id)

        with self.db_conn.cursor() as cur:
            cur.execute(
                f"UPDATE users SET {set_clause} WHERE id = %s RETURNING *", tuple(values))
            updated_user = cur.fetchone()
            if not updated_user:
                raise NotFoundError("User not found.")
            self.db_conn.commit()

    def delete_user(self, user_id: int) -> User:
        """
        Delete a user from the database by user ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s RETURNING *", (user_id,))
            self.db_conn.commit()
            res = cur.fetchone()
            if not res:
                raise NotFoundError("User not found.")
            return map_result_to_entity(User, res, cur)
