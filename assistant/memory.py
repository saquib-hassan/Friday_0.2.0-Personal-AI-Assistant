import os
import json

class Memory:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(base_dir, "memory.json")

        self.history = []

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []

    def add(self, role, message):

        entry = {
            "role": role,
            "message": message
        }

        self.history.append(entry)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def get_history(self):

        text = ""
        for item in self.history:
            text += f"{item['role']}: {item['message']}\n"

        return text
