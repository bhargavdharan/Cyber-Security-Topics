import pymysql
from config import Config

def get_db_connection():
    """Get a MySQL database connection."""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4'
    )

def execute_query(query, params=None, fetch_one=False):
    """Execute a query and return results."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    return cursor.fetchone()
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()
