class Conversation():
    def __init__(self, from_number, to_number, messages):
        self.messages = []
        self.from_number = from_number
        self.to_number = to_number
        self.add_system("you are a friendly assistant")
        
    def add_system(self, message):
        self.messages.append({"role" : "system", "content": message})

    def change_system(self, message):
        self.messages[0]['content'] = message
    
    def reset_system(self, message):
        self.messages = []
        self.add_system(message)
        
    def add_role_user(self, message):
        self.messages.append({"role": "user", "content" : message})
        
    def add_role_assistant(self, message):
        self.messages.append({"role" : "assistant", "content" : message})
    
    def get_from(self):
        return self.from_number
    
    def get_to(self):
        return self.to_number
        
    def __str__(self):
        return f"user{self.from_number}"

    def __repr__(self):
        return f"user{self.from_number}"
        
    def process(self, func, message):
        self.response = func(message)
        self.add_role_user(message)
        self.add_role_assistant(self.response)
        return self.response


