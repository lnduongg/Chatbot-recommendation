import psycopg2
from app.core.config import settings

new_DB_NAME = settings.DB_NAME

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE {new_DB_NAME};")
    print(f"Database '{new_DB_NAME}' được tạo thành công!")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Lỗi khi tạo database: {e}")