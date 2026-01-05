import bcrypt
from db.database import Database

class AuthService:

    @staticmethod
    def register(email, password):
        db = Database()

        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

        try:
            db.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password_hash)
            )
            return True
        except:
            return False
        finally:
            db.close()

    @staticmethod
    def login(email, password):
        db = Database()

        user = db.fetch_one(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )
        db.close()

        if not user:
            return False

        return bcrypt.checkpw(
            password.encode(),
            user["password_hash"].encode()
        )
