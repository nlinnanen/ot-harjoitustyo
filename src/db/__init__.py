import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


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
