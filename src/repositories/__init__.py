import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from repositories.member_repository import MemberRepository
from repositories.user_repository import UserRepository

def create_db_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

conn = create_db_conn()
user_repository = UserRepository(conn)
member_repository = MemberRepository(conn)
