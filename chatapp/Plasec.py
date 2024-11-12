import logging

logging.getLogger("sagemaker").setLevel(logging.ERROR)
class Plasec:
    def __init__(self, chat, topic, system,script=""):
         
        self.chat = chat  # could be a list of messages or a string
        self.topic = topic
        self.system = system
        self.script=self.setscript(script)
  
    def get_chat(self):
        """Returns the chat history."""
        return self.chat
    def setscript(self,title):
         if title=="cal":
           return cal.py
    def get_topic(self):
        """Returns the current topic of the chat."""
        return self.topic
    
    def get_system(self):
        """Returns the system information."""
        return self.system
    
    def add_message(self, message):
        """Adds a new message to the chat history."""
        if isinstance(self.chat, list):
            self.chat.append(message)
        else:
            self.chat += "\n" + message
   
    def set_topic(self, new_topic):
        """Changes the topic of the chat."""
        self.topic = new_topic
    
    def __str__(self):
        """Returns a string representation of the chat session."""
        return f"Topic: {self.topic}\nSystem: {self.system}\nChat: {self.chat}"

# Example usage
 
session = ChatSession(["Hello, how can I help?", "Tell me about AI."], "AI discussion", "ChatbotSystem v1")

print(session.get_chat())
print(session.get_topic())
print(session.get_system())

session.add_message("Sure, AI stands for Artificial Intelligence.")
print(session)
