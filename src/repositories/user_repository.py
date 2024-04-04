import psycopg2

from entities.user import User


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
            return User(*user_data) if user_data else None
    
    def get_user_by_email(self, email):
        """
        Fetch a single user by their email.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            return User(*user_data) if user_data else None
        
    def get_all_users(self):
        """
        Fetch all users from the database.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            return [User(*u) for u in users]
   
    
    def add_user(self, user: User) -> str:
      """
      Add a new user to the database.
      """
      with self.db_conn.cursor() as cur:
        cur.execute(
          "INSERT INTO users (email, password, admin) VALUES (%s, %s, %s) RETURNING id", (user.email, user.password, user.admin))
        self.db_conn.commit()
        user_id = cur.fetchone()[0]
        return user_id

    def update_user(self, user: User):
        """
        Update user details based on provided keyword arguments.
        """
        set_clause = ', '.join([f"{key} = %s" for key in user.__dict__])
        values = list(user.__dict__.values())
        values.append(user.id)

        with self.db_conn.cursor() as cur:
            cur.execute(
                f"UPDATE users SET {set_clause} WHERE id = %s", tuple(values))
            self.db_conn.commit()

    def delete_user(self, user: User):
        """
        Delete a user from the database by user ID.
        """
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user.id,))
            self.db_conn.commit()
