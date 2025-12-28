import os
import json

class Memory:
    def __init__(self):
        self.file_path = "H://Friday_0.2.0-Personal-AI-Assistant//assistant//memory.json"
        self.history = []
        if os.path.exists(self.file_path):
            with open(self.file_path,"r") as j:
               self.history= json.load(j)
        else:
            self.history = []

    
    def add(self,role,message):
        pass

    def get_history(self):
        pass