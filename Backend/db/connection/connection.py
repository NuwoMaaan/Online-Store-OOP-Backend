from mysql.connector import pooling, Error
from db.connection.config import settings

_pool = None

def init_pool(pool_name="mypool", pool_size=5, **dbconfig):
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size, **dbconfig)

def connection():
    global _pool
    if _pool is None:
        init_pool(
            host=settings.HOST,
            user=settings.USER,
            password=settings.PASSWORD,
            database=settings.DATABASE,
            pool_size=settings.POOL_SIZE,
        )
    try:
        return _pool.get_connection()
    except Error as err:
        print(f"Error getting connection from pool: {err}")
        return None

