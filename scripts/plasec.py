import cohere
import sys
import getpass
import os
 
class Plasec:
    def __init__(self, chat, topic, system, script=""):
        self.chat = chat  # could be a list of messages or a string
        self.topic = topic
        self.system = system
        self.script = self.setscript(script)

        # Initialize the Cohere client here
        API_KEY = 'oef7WXPGxfMecqTtsvR5OHaFORkxC9UqH9YGJPZn'
        co = cohere.Client(API_KEY)
       
 
        try:
            response = co.generate(
                model="command",
                prompt=self.chat,
                temperature=0.9
            )
            self.answer = response.generations[0].text
        except Exception as e:
            self.answer = f"Error: {str(e)}"

    def setscript(self, title):
        if title == "cal":
            return "cal.py"
        return title

    def __str__(self):
        return f"Topic: {self.topic}\nSystem: {self.system}\nChat: {self.chat}\nAnswer: {self.answer}"

if __name__ == "__main__":
    try:
        chat = sys.argv[1]
        topic = sys.argv[2]
        system = sys.argv[3]
        plasec_instance = Plasec(chat, topic, system)
        print(plasec_instance.answer)
    except Exception as e:
        print(f"Error in model: {str(e)}")
