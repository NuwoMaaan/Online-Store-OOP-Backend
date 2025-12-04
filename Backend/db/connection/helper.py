from contextlib import contextmanager
from db.connection.connection import connection

@contextmanager
def get_cursor(dictionary=True):
    conn = connection()
    if conn is None:
        yield None
        return
    cur = conn.cursor(dictionary=dictionary)
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()  # returns connection to pool