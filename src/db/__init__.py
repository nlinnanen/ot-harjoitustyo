import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from db.member_repository import MemberRepository
from db.user_repository import UserRepository


def create_db_conn(port=DB_PORT):
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=port
    )


def delete_db_contents(_conn=create_db_conn()):
    with _conn.cursor() as cur:
        cur.execute("DELETE FROM members")
        cur.execute("DELETE FROM users")
        _conn.commit()


conn = create_db_conn()
user_repository = UserRepository(db_conn=conn)
member_repository = MemberRepository(db_conn=conn)