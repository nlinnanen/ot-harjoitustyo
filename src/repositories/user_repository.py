import psycopg2


class UserRepository:
    def __init__(self, db_conn):
        """
        Initialize the repository with a database connection.
        :param db_conn: A database connection object.
        """
        self.db_conn = db_conn

    def get_user_by_id(self, user_id):
        """
        Fetch a single user by their user ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            return user_data if user_data else None
        
    def get_all_users(self):
        """
        Fetch all users from the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            return users
   
    
    def add_user(self, email: str, password: str) -> str:
      """
      Add a new user to the database.
      """
      with self.db_conn.cursor() as cur:
        cur.execute(
          "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id", (email, password))
        self.db_conn.commit()
        user_id = cur.fetchone()[0]
        return user_id

    def update_user(self, user_id, **kwargs):
        """
        Update user details based on provided keyword arguments.
        """
        set_clause = ', '.join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values())
        values.append(user_id)

        with self.db_conn.cursor() as cur:
            cur.execute(
                f"UPDATE users SET {set_clause} WHERE id = %s", tuple(values))
            self.db_conn.commit()

    def delete_user(self, user_id):
        """
        Delete a user from the database by user ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db_conn.commit()
