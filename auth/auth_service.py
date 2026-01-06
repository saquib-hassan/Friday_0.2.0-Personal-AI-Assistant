import bcrypt
from db.database import Database


class AuthService:
    """
    Handles user authentication logic
    """

    def register_user(self, email: str, password: str) -> bool:
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        db = Database()

        query = """
        INSERT INTO users (email, password_hash)
        VALUES (%s, %s)
        """

        try:
            db.execute(query, (email, password_hash))
            return True
        except Exception as e:
            print("Registration error:", e)
            return False
        finally:
            db.close()

    def login_user(self, email: str, password: str) -> bool:
        db = Database()

        query = "SELECT password_hash FROM users WHERE email = %s"
        user = db.fetch_one(query, (email,))
        db.close()

        if not user:
            return False

        return bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )
