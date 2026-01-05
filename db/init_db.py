from db.database import Database


def create_tables():
    db = Database()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    db.execute(create_users_table)
    db.close()

    print("Database & users table ready")


if __name__ == "__main__":
    create_tables()

