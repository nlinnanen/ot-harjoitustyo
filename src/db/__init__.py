import sqlite3
from db.member_repository import MemberRepository
from db.user_repository import UserRepository

def init_db(connection):
    cursor = connection.cursor()

    with open('schema.sql', 'r', encoding="UTF-8") as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    try:
        cursor.execute(
            "INSERT INTO users (email, password, admin) VALUES (?, ?, ?)",
            ("admin@admin.com", "admin", 1)
        )
    except sqlite3.IntegrityError:
        pass

    connection.commit()

def create_db_conn(filename='database.db'):
    connection = sqlite3.connect(filename)
    init_db(connection)
    return connection


def delete_db_contents(_conn=create_db_conn()):
    cursor = _conn.cursor()
    cursor.execute("DELETE FROM members")
    cursor.execute("DELETE FROM users")
    _conn.commit()


conn = create_db_conn()
user_repository = UserRepository(db_conn=conn)
member_repository = MemberRepository(db_conn=conn)
