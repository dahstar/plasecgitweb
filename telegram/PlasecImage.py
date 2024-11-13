import shlex
import requests
import json
import metisai
import os
import time

class PlasecImage:
    def __init__(self):
        # Set up API key and bot ID from environment variables
        self.api_key = os.getenv('METIS_API_KEY')
        self.bot_id = os.getenv('METIS_BOT_ID_IMAGE')

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
            print(f"Error: {e}")
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
            print(f"Error: {e}")
            return None

    def get_image(self, prompt):
        # Check if API key and bot ID are available
        if not self.api_key or not self.bot_id:
            print("API key or Bot ID not found. Please set METIS_API_KEY and METIS_BOT_ID_IMAGE.")
            return None

        # Create MetisBot instance and session
        metisbot = metisai.MetisBot(api_key=self.api_key, bot_id=self.bot_id)
        session_id = metisbot.create_session().id
        task_id = self.generate_image_with_metis(session_id, prompt)
        
        if task_id:
            print("Generated Task ID:", task_id)

            # Polling the task status until it's finished
            while True:
                task_status = self.check_task_status(session_id, task_id)
                if task_status:
                    if task_status.get("status") == "FINISHED":
                        print("Task finished!")
                        attachments = task_status.get("message", {}).get("attachments", [])
                        if attachments:
                            image_url = attachments[0].get("content")
                            return image_url
                        else:
                            print("No attachments found.")
                        break
                    elif task_status.get("status") == "FAILED":
                        print("Task failed.")
                        break
                    else:
                        print("Task is still running, checking again in 5 seconds...")
                        time.sleep(5)
                else:
                    print("Failed to get task status.")
                    break
        else:
            print("Failed to generate task ID.")
        return "No URL found"

if __name__ == "__main__":
    d = PlasecImage()
    s = input("prompt: ")
    prompt = "/imagine " + s
    image_url = d.get_image(prompt)
    print("Image URL:", image_url)
