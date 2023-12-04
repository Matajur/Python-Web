from contextlib import contextmanager

from psycopg2 import connect, DatabaseError


@contextmanager
def connection():
    conn = None
    try:
        conn = connect(
            host="localhost", user="postgres", database="postgres", password="qwerty123"
        )
        yield conn
        conn.commit()
    except DatabaseError as err:
        print(err)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
