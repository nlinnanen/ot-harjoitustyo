import sqlite3
from typing import Generator
from db.utils import NotCreatedError, NotFoundError, map_result_to_entity, require_id
from entities.member import Member


class MemberRepository:
    def __init__(self, db_conn: sqlite3.Connection):
        """
        Initialize the repository with a database connection.
        """
        self.db_conn = db_conn

    def get_member_by_id(self, member_id: int) -> Member:
        """
        Fetch a single member by their member ID.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        member_data = cursor.fetchone()
        cursor_description = cursor.description
        cursor.close()
        if not member_data:
            raise NotFoundError("Member not found.")
        return map_result_to_entity(Member, member_data, cursor_description)

    def get_member_by_user_id(self, user_id: int) -> Member:
        """
        Fetch a single member by their user ID.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM members WHERE user_id = ?", (user_id,))
        member_data = cursor.fetchone()
        cursor_description = cursor.description
        cursor.close()
        if not member_data:
            raise NotFoundError("Member not found.")
        return map_result_to_entity(Member, member_data, cursor_description)

    def get_all_members(self) -> "Generator[Member, None, None]":
        """
        Fetch all members from the database.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM members")
        cursor_description = cursor.description
        for member in cursor:
            yield map_result_to_entity(Member, member, cursor_description)
        cursor.close()

    def add_member(self, new_member: Member) -> Member:
        """
        Add a new member to the database.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(
            """INSERT INTO members (
                first_name,
                last_name,
                start_year,
                member_until,
                home_municipality,
                user_id
            )
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                new_member.first_name,
                new_member.last_name,
                new_member.start_year,
                new_member.member_until,
                new_member.home_municipality,
                new_member.user_id
            )
        )
        new_member_id = cursor.lastrowid
        self.db_conn.commit()
        cursor.execute("SELECT * FROM members WHERE id = ?", (new_member_id,))
        added_member = cursor.fetchone()
        cursor_description = cursor.description
        cursor.close()
        if not added_member:
            raise NotCreatedError("Member not created.")
        return map_result_to_entity(Member, added_member, cursor_description)

    @require_id
    def update_member(self, member: Member):
        """
        Update member details based on provided keyword arguments.
        """
        set_clause = ', '.join([f"{key} = ?" for key in member.__dict__ if key != 'id'])
        values = [member.__dict__[key] for key in member.__dict__ if key != 'id']
        values.append(member.id)
        cursor = self.db_conn.cursor()
        cursor.execute(
            f"UPDATE members SET {set_clause} WHERE id = ?", values)
        num_updated = cursor.rowcount
        cursor.close()
        if num_updated == 0:
            raise NotFoundError("Member not found.")
        self.db_conn.commit()

    def delete_member(self, member_id: int):
        """
        Delete a member from the database by member ID.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        deleted_member = cursor.fetchone()
        if not deleted_member:
            cursor.close()
            raise NotFoundError("Member not found.")

        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.db_conn.commit()
        cursor.close()
