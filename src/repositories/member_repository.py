

class MemberRepository:
    def __init__(self, db_conn):
        """
        Initialize the repository with a database connection.
        :param db_conn: A database connection object.
        """
        self.db_conn = db_conn

    def get_member_by_id(self, member_id):
        """
        Fetch a single member by their member ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            member_data = cur.fetchone()
            return member_data if member_data else None

    def get_all_members(self):
        """
        Fetch all members from the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM members")
            members = cur.fetchall()
            return members

    def add_member(self, first_name, last_name, start_year, member_until, home_municipality, user_id):
        """
        Add a new member to the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO members (first_name, last_name, start_year, member_until, home_municipality, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (first_name, last_name, start_year, member_until, home_municipality, user_id)
            )
            self.db_conn.commit()
            member_id = cur.fetchone()[0]
            return member_id

    def update_member(self, member_id, **kwargs):
        """
        Update member details based on provided keyword arguments.
        """
        set_clause = ', '.join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values())
        values.append(member_id)

        with self.db_conn.cursor() as cur:
            cur.execute(
                f"UPDATE members SET {set_clause} WHERE id = %s", tuple(values))
            self.db_conn.commit()
    
    def delete_member(self, member_id):
        """
        Delete a member from the database by member ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM members WHERE id = %s", (member_id,))
            self.db_conn.commit()