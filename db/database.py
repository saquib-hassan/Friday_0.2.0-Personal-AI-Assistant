
import mysql.connector
from config.settings import Settings


class Database:
    def __init__(self):
        settings = Settings()

        self.connection = mysql.connector.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
