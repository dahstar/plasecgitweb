#API_KEY = '67OnhuU6Mhp1x6PcEoK9WJ5Vl5p4bn90Y3gB1u2J'
#import cohere
import sys
import getpass
import os
import metisai
import secrets
import tiktoken

class Plasec:
    def __init__(self, chat, topic, system, script=""):
        self.metisbot = metisai.MetisBot(api_key='tpsg-IEhiVTXtW43awN3iSvA88I1CYyVsE48', bot_id='323bd747-4765-427b-bb4f-8f1c9be07bc7')
        # Ensure chat is a string; extract 'text' from chat if it is a dict or object
        if isinstance(chat, dict):
            if 'text' in chat:
                self.chat = chat['text'][:512]  # Extract the message text and limit to 512 characters
            else:
                raise ValueError("Chat object does not contain 'text' key")
        else:
            self.chat = chat if isinstance(chat, str) else str(chat)
        
        self.topic = topic
        self.system = system
        self.script = self.setscript(script)
        self.token = self.generate_token()
        self.count=self.num_tokens_from_messages(self.chat)
        API_KEY = os.environ.get('COHERE_API_KEY')
        print("aaa",API_KEY)
        #co = cohere.Client(API_KEY)
        try:
            '''
            # Generate response using Cohere API
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=self.chat,  # Ensure this is a string and within limits
                max_tokens=100,
                temperature=0.8
            )
            self.answer = response.generations[0].text'''
            self.get_metis(self.chat)
        except Exception as e:
            self.answer = f"Error: {str(e)}"
        
          
    def num_tokens_from_messages(self,messages, model="gpt-3.5-turbo-0125"):
     """Returns the number of tokens used by a list of messages."""
     try:
        encoding = tiktoken.encoding_for_model(model)
     except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
     if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
     elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
     elif model == "gpt-3.5-turbo-0613":
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
     elif model == "gpt-4-0613":
        return num_tokens_from_messages(messages, model="gpt-4-0314")
     num_tokens = 0#gpt-3.5-turbo-0125
     for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
     num_tokens += 2  # every reply is primed with <im_start>assistant
     return num_tokens   
    def split_message(self,message, chunk_size=512):
     """Splits a long message into smaller chunks of the given size."""
     return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
    
    def get_metis(self,message):
     # Initialize a session
     session = self.metisbot.create_session()
     message = self.metisbot.send_message(session, message)
     self.answer=message.content
     # Delete a session
     self.metisbot.delete_session(session)    
    def generate_token(self, length=32):
        """Generates a secure random token of the specified length."""
        return secrets.token_urlsafe(length)

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
