import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, use_db=True):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        self.cursor = self.connection.cursor()

        if use_db:
            self.create_database()
            self.cursor.execute("USE friday_db")

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS friday_db")

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
