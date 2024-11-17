import os
import time
import requests
import metisai

class PlasecImage:
    def __init__(self):
        # Set up API key and bot ID from environment variables
        self.api_key = os.getenv('METIS_API_KEY')
        self.bot_id = os.getenv('METIS_BOT_ID_IMAGE')
        self.url = ""

    def generate_image_with_metis(self, session_id, prompt):
        url = f"https://api.metisai.ir/api/v1/chat/session/{session_id}/message/async"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
            print(f"Error generating task: {e}")
            return None

    def check_task_status(self, session_id, task_id):
        url = f'https://api.metisai.ir/api/v1/chat/session/{session_id}/message/async/{task_id}'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error checking task status: {e}")
            return None
    def get_prompt(self,prompt):
   
     prompt = "/imagine " + prompt
     url = self.get_image(prompt)
     return url
    def get_image(self, prompt):
        # Check if API key and bot ID are available
        if not self.api_key or not self.bot_id:
            print("API key or Bot ID not found. Please set METIS_API_KEY and METIS_BOT_ID_IMAGE.")
            return None

        # Create MetisBot instance and session
        metisbot = metisai.MetisBot(api_key=self.api_key, bot_id=self.bot_id)
        session_id = metisbot.create_session().id
        task_id = self.generate_image_with_metis(session_id, prompt)
        
        if not task_id:
            print("Failed to generate task ID.")
            return None

        print("Generated Task ID:", task_id)

        # Polling the task status until it's finished or failed
        while True:
            task_status = self.check_task_status(session_id, task_id)
            if task_status:
                status = task_status.get("status")
                if status == "FINISHED":
                    print("Task finished!")
                    attachments = task_status.get("message", {}).get("attachments", [])
                    if attachments:
                        image_url = attachments[0].get("content")
                        return image_url

                    else:
                        print("No attachments found.")
                        return None
                elif status == "FAILED":
                    print("Task failed.")
                    return None
                else:
                    print("Task is still running, checking again in 5 seconds...")
                    time.sleep(5)
            else:
                print("Failed to get task status.")
                return None

if __name__ == "__main__":
    d = PlasecImage()
    s = input("Prompt: ")
    prompt = "/imagine " + s
    d.url = d.get_image(prompt)
    print("Image URL:", d.url)
