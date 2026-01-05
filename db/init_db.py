import mysql.connector
from config.settings import Settings

settings = Settings()

conn = mysql.connector.connect(
    host=settings.db_host,
    user=settings.db_user,
    password=settings.db_password
)
cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.db_name}")
cursor.execute(f"USE {settings.db_name}")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cursor.close()
conn.close()

print("Database & users table created")
