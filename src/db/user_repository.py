import sqlite3
from typing import Generator
from entities.user import User
from db.member_repository import require_id
from db.utils import NotCreatedError, NotFoundError, map_result_to_entity

class UserRepository:
    def __init__(self, db_conn: sqlite3.Connection):
        """
        Alustaa repositorion annetulla tietokantayhteydellä.
        """
        self.db_conn = db_conn

    def get_user_by_id(self, user_id: int) -> User:
        """
        Hakee käyttäjän tietokannasta käyttäjän ID:n perusteella.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            cursor.close()
            raise NotFoundError("Käyttäjää ei löydy.")
        cursor_description = cursor.description
        cursor.close()
        return map_result_to_entity(User, user_data, cursor_description)

    def get_user_by_email(self, email: str) -> User:
        """
        Hakee käyttäjän tietokannasta sähköpostiosoitteen perusteella.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        if not user_data:
            cursor.close()
            raise NotFoundError("Käyttäjää ei löydy.")
        cursor_description = cursor.description
        cursor.close()
        return map_result_to_entity(User, user_data, cursor_description)

    def get_all_users(self) -> "Generator[User, None, None]":
        """
        Palauttaa generaattorin, joka iteroi kaikki käyttäjät tietokannasta.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users")
        cursor_description = cursor.description
        for user in cursor:
            yield map_result_to_entity(User, user, cursor_description)
        cursor.close()

    def add_user(self, user: User) -> User:
        """
        Lisää uuden käyttäjän tietokantaan ja palauttaa lisätyn käyttäjän.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password, admin) VALUES (?, ?, ?)",
            (user.email, user.password, user.admin)
        )
        user_id = cursor.lastrowid
        self.db_conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        added_user = cursor.fetchone()
        if not added_user:
            cursor.close()
            raise NotCreatedError("Käyttäjän luonti epäonnistui.")
        cursor_description = cursor.description
        cursor.close()
        return map_result_to_entity(User, added_user, cursor_description)

    @require_id
    def update_user(self, user: User):
        """
        Päivittää olemassa olevan käyttäjän tiedot tietokannassa.
        """
        set_clause = ', '.join([f"{key} = ?" for key in user.__dict__ if key != 'id'])
        values = [user.__dict__[key] for key in user.__dict__ if key != 'id']
        values.append(user.id)
        cursor = self.db_conn.cursor()
        cursor.execute(
            f"UPDATE users SET {set_clause} WHERE id = ?", values)
        self.db_conn.commit()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user.id,))
        updated_user = cursor.fetchone()
        if not updated_user:
            cursor.close()
            raise NotFoundError("Käyttäjää ei löydy.")
        cursor_description = cursor.description
        cursor.close()
        return map_result_to_entity(User, updated_user, cursor_description)

    def delete_user(self, user_id: int):
        """
        Poistaa käyttäjän tietokannasta käyttäen käyttäjän ID:tä.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            raise NotFoundError("Käyttäjää ei löydy.")

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db_conn.commit()
        cursor.close()
