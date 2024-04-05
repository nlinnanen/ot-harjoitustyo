

from typing import Generator
from db.utils import NotCreatedError, NotFoundError, map_result_to_entity, require_id
from entities.member import Member

from psycopg2.extensions import connection

class MemberRepository:
    def __init__(self, db_conn: connection):
        """
        Initialize the repository with a database connection.
        :param db_conn: A database connection object.
        """
        self.db_conn = db_conn

    def get_member_by_id(self, member_id: int) -> Member:
        """
        Fetch a single member by their member ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            member_data = cur.fetchone()
            if not member_data:
                raise NotFoundError("Member not found.")
            return map_result_to_entity(Member, member_data, cur)

    def get_all_members(self) -> "Generator[Member, None, None]":
        """
        Fetch all members from the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM members")
            for member in cur:
                yield map_result_to_entity(Member, member, cur)

    def add_member(self, new_member: Member) -> Member:
        """
        Add a new member to the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO members (first_name, last_name, start_year, member_until, home_municipality, user_id) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        RETURNING *
                    """,
                        **new_member.__dict__
                        )
            self.db_conn.commit()
            added_member = cur.fetchone()
            if not added_member:
                raise NotCreatedError("Member not created.")
            return map_result_to_entity(Member, added_member, cur)

    @require_id
    def update_member(self, member: Member):
        """
        Update member details based on provided keyword arguments.
        """

        set_clause = ', '.join([f"{key} = %s" for key in member.__dict__])

        with self.db_conn.cursor() as cur:
            cur.execute(
                f"UPDATE members SET {set_clause} WHERE id = %s", member.id
            )
            num_updated = cur.rowcount
            if num_updated == 0:
                raise NotFoundError("Member not found.")
            self.db_conn.commit()

    @require_id
    def delete_member(self, member: Member):
        """
        Delete a member from the database by member ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM members WHERE id = %s RETURNING *", (member.id,))
            delted_member = cur.fetchone()
            if not delted_member:
                raise NotFoundError("Member not found.")
            self.db_conn.commit()
