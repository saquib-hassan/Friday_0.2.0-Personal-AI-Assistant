from db.database import Database


class Memory:
    """
    Stores and retrieves conversation history from database.
    Each user has their own conversation history.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.history = self._load_history()

    def _load_history(self):
        """Load conversation history from database."""
        db = Database()
        query = """
        SELECT role, message
        FROM conversations
        WHERE user_id = %s
        ORDER BY created_at ASC
        """
        db.cursor.execute(query, (self.user_id,))
        rows = db.cursor.fetchall()
        db.close()
        return [{"role": row["role"], "message": row["message"]} for row in rows]

    def add(self, role: str, message: str):
        """Add a message to conversation history."""
        db = Database()
        query = """
        INSERT INTO conversations (user_id, role, message)
        VALUES (%s, %s, %s)
        """
        db.execute(query, (self.user_id, role, message))
        db.commit()
        db.close()

        self.history.append({"role": role, "message": message})

    def get_history(self):
        """Get formatted conversation history as text."""
        text = ""
        for item in self.history:
            text += f"{item['role']}: {item['message']}\n"
        return text

    def clear(self):
        """Clear conversation history for this user only."""
        db = Database()
        query = "DELETE FROM conversations WHERE user_id = %s"
        db.execute(query, (self.user_id,))
        db.commit()
        db.close()
        self.history = []
