import os
import json

class Memory:
    """
    Stores and retrieves conversation history
    """

    def __init__(self):
        self.file_path = "assistant/memory.json"
        self.history = []

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.history = json.load(f)

    def add(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

        with open(self.file_path, "w") as f:
            json.dump(self.history, f)

    def get_history(self):
        text = ""
        for item in self.history:
            text += f"{item['role']}: {item['message']}\n"
        return text
