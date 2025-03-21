import pymysql


async def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
