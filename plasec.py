import sys
import getpass
import os
import metisai
import secrets
import tiktoken
import requests
import uuid
import  PlasecImage   


class Plasec:
    def __init__(self, chat, topic="", system="", answer="",script="",action="text"):
        self.METIS_API_KEY=os.getenv('METIS_API_KEY')
        self.METIS_BOT_ID=os.getenv('METIS_BOT_ID')
        self.metisbot = metisai.MetisBot(api_key=self.METIS_API_KEY, bot_id=self.METIS_BOT_ID)
        self.answer="error"
        
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
        #self.count=self.num_tokens_from_messages(self.chat)
        #print("aaa",API_KEY)
        #co = cohere.Client(API_KEY)
        try:
          if action=="generate_image":
             imagep=PlasecImage.PlasecImage()
             self.answer=imagep.get_image(chat)
             return 
          elif answer=="":
             self.get_metis(self.chat)
          else:
              self.answer=answer
          self.token=self.token+"-"+str(self.get_price())+"$"
        except Exception as e:
            self.answer = f"Error: {str(e)}"
    def check_task_status(self,session_id, task_id, api_key):
     url = f'https://api.metisai.ir/api/v1/chat/session/{session_id}/message/async/{task_id}'
     headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
     }
     try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
     except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    def generate_image_with_metis(self,session_id, api_key, prompt):
     url = f"https://api.metisai.ir/api/v1/chat/session/{session_id}/message/async"
     headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
     }
     data = {
        "message": {
            "content": prompt,
            "type": "USER"
        }
     }
     try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()
        task_id = response_data.get("taskId")
        print("Task ID:", task_id)
        return task_id
     except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    def get_image(self,prompt):
     # Environment variables for API key and bot ID
     api_key = os.getenv('METIS_API_KEY')
     bot_id = os.getenv('METIS_BOT_ID_IMAGE')
     # Create MetisBot instance and session
     metisbot = metisai.MetisBot(api_key=api_key, bot_id=bot_id)
     session_id = metisbot.create_session().id
     task_id = self.generate_image_with_metis(session_id, api_key, prompt)
     if task_id:
      print("Generated Task ID:", task_id)
    
     # Polling the task status until it's finished
     while True:
        task_status = self.check_task_status(session_id, task_id, api_key)
        if task_status:
            # Check if the task is finished
            if task_status.get("status") == "FINISHED":
                print("Task finished!")
                # Extract and print the image URL
                attachments = task_status.get("message", {}).get("attachments", [])
                if attachments:
                    image_url = attachments[0].get("content")
                    return image_url
                else:
                    print("No attachments found.")
                break
            elif task_status.get("status") == "FAILED":
                print("Task failed.")
                
            else:
                print("Task is still running, checking again in 5 seconds...")
               
        else:
            print("Failed to get task status.")
            break
     else:
       print("Failed to generate task ID.")
     print("no url")          
    def request_to_metis(self,prompt, api_Key, model_provider, model_name):
     metis_url = 'https://api.metisai.ir/api/v1/chat/{provider}/completions'

     # construct the headers for the request
     headers = {
        "x-api-key": api_Key,
        "Content-Type": "application/json"
     }

     # Payload for the request
     data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that translates English subtitle of a movie to Persian."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
     }

     # Construct the full API endpoint URL with the provider
     url = metis_url.replace('{provider}', model_provider)

     # Make the POST request to Metis API
     response = requests.post(url, headers=headers, json=data)

     # Parse the response JSON and return the result
     if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
     else:  # Check for errors
        raise Exception(f"Failed to get response from Metis API: {response.text}")

    def geenrate_image(self, chat, topic="", system="", answer="",script="",):
        self.METIS_BOT_ID_IMAGE=os.getenv('METIS_BOT_ID_IMAGE')
        self.metisbot = metisai.MetisBot(api_key=self.METIS_API_KEY ,bot_id=self.METIS_BOT_ID_IMAGE)
        # Ensure chat is a string; extract 'text' from chat if it is a dict or object
       
        self.chat = chat 
        self.topic = topic
        self.system = system
        self.script = self.setscript(script)
        self.token = self.generate_token()
        #self.count=self.num_tokens_from_messages(self.chat)
        #print("aaa",API_KEY)
        #co = cohere.Client(API_KEY)
        try:
           
            if answer=="":
             self.get_metis(self.chat)
            else:
              self.answer=answer
            self.token=self.token+"-"+str(self.get_price())+"$"
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
    def get_metis_curl(self,message):
        url = "https://metisai.ir/api/endpoint"  # Replace with the correct endpoint
        headers = {
    "Authorization": 'tpsg-IEhiVTXtW43awN3iSvA88I1CYyVsE48',
    "Content-Type": "application/json"
}
        data = {
        "message": "Your message here"
}

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
          response_data = response.json()
          print("Response:", response_data)
        else:
           print("Error:", response.status_code, response.text)
    def get_price(self,message="",type=""):
        messagesin = [{"role": "user", "content": self.chat}]
        messagesout = [{"role": "user", "content": self.answer}]
        if message!="":
         messages = [{"role": "user", "content": messgae}]
         messagesin=messages
         messagesout=messages
        pricein= int(self.num_tokens_from_messages(messagesin)) * 0.0000006
        priceout=int(self.num_tokens_from_messages(messagesout)) * 0.00001
        if type=="in": 
           return pricein
        elif type=="out":
           return priceout
        else:
          return pricein+priceout
     
    def get_metis(self, message_content):
     session = self.metisbot.create_session()

     # Initialize a session
     unique_id = str(uuid.uuid4())

     # Construct the message in the expected format
     message = {
        "id": unique_id,  # Unique identifier
        "content": message_content,     # The actual message content
        "role": "user" ,                 # Depending on the context, this might be "user" or "assistant"
        "type":"general"
        }
    
     # Send the message
     response = self.metisbot.send_message(session, message_content)
    
     # Extract the answer
     self.answer = response.content  # Adjust this based on how the response is structured
    
     # Delete the session
     self.metisbot.delete_session(session)
    def get_metis1(self,message):
     # Initialize a session
     session = self.metisbot.create_session()
     message = self.metisbot.send_message(session, [message])
     self.answer=message.content
     # Delete a session
    def generate_token(self, length=16):
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
        chat =  input("chat")
        topic =  input("topic")
        system = input("system")
        plasec_instance = Plasec(chat, topic, system)
        if "Error:" in plasec_instance.answer:
             plasec_instance.answer=plasec_instance.get_metis1(chat)
        print(plasec_instance.answer)
    except Exception as e:
        print(f"Error in model: {str(e)}")
