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
        """
        Docstring for add
        
        :param self: It expects an obeject
        :param role: User role
        :param message: I've created a message dictionary and appened it to history list and 
                        open json as write mode and save the history later.
        """
        self.message = {"role":role, "message": message}
        self.history.append(self.message)

        with open(self.file_path,"w") as w:
            json.dump(self.history,w)

        

    def get_history(self):
        pass