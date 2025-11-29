from mysql.connector import pooling, Error

_pool = None

def init_pool(pool_name="mypool", pool_size=5, **dbconfig):
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size, **dbconfig)

def connection():
    global _pool
    if _pool is None:
        init_pool(
            host="localhost",
            user="root",
            password="Pa55w.rd",
            database="online_store",
            pool_size=5,
        )
    try:
        return _pool.get_connection()
    except Error as err:
        print(f"Error getting connection from pool: {err}")
        return None

