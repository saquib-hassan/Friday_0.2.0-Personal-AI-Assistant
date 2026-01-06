import bcrypt
from db.database import Database


class AuthService:
    """
    Handles user authentication:
    - register
    - login
    """

    def email_exists(self, email: str) -> bool:
        """Check if an email is already registered."""
        email = email.strip().lower()
        db = Database()

        query = "SELECT id FROM users WHERE email = %s"
        user = db.fetch_one(query, (email,))
        db.close()

        return user is not None

    def register_user(self, email: str, password: str) -> bool:
        email = email.strip().lower()

        # Explicit check for existing email
        if self.email_exists(email):
            return False

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
            db.commit()
            return True
        except Exception as e:
            # print("Registration error:", e)
            return False
        finally:
            db.close()

    def login_user(self, email: str, password: str):
        """
        Returns (user_id, email) on success, or None on failure.
        """
        email = email.strip().lower()

        db = Database()

        query = """
        SELECT id, email, password_hash
        FROM users
        WHERE email = %s
        """

        user = db.fetch_one(query, (email,))
        db.close()

        if not user:
            return None

        if bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):
            return (user["id"], user["email"])

        return None

