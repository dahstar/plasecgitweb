 
import subprocess
from django.shortcuts import render, redirect
 
from chatapp.forms import ChatMessageForm
from .models import ChatMessage
from django.http import JsonResponse
import requests

from django.utils import timezone
import cohere
import getpass
import os
import sqlite3
from .models import ChatMessage  # Assuming Message is the model for messages
from django.views.decorators.csrf import csrf_exempt
import requests

from langchain_cohere import ChatCohere
os.environ["COHERE_API_KEY"] = "oef7WXPGxfMecqTtsvR5OHaFORkxC9UqH9YGJPZn"

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate

chat_model = ChatCohere()

topic='default_topic' 
API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(API_KEY)

system='default_system'
texamples=[]
def initialize_db():
    # Connect to the SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS examples (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        type TEXT NOT NULL DEFAULT 'general', -- Default type is 'general'
                        system TEXT NOT NULL DEFAULT 'default_system' -- Default system
                      )''')

    # Commit and close connection
    conn.commit()
    conn.close()
def add_question(question, answer, q_type='general', system='default_system'):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()

    # Insert new question into the table
    cursor.execute('''INSERT INTO examples (question, answer, type, system) 
                      VALUES (?, ?, ?, ?)''', (question, answer, q_type, system))

    conn.commit()
    conn.close()
def get_examples_by_type(q_type='general'):
    conn = sqlite3.connect('train.db')
    cursor = conn.cursor()

    # Retrieve examples of a specific type
    cursor.execute('''SELECT question, answer FROM examples WHERE type = ?''', (q_type,))
    examples = cursor.fetchall()

    conn.close()
    return examples

def addexaample(question, answer, q_type='general', system='default_system'):
    # Add the new example to the database
    add_question(question, answer, q_type, system)
def gettrainedmodel(message, task_type="train"):
    # Fetch examples from the database based on the task type
    examples = get_examples_by_type(task_type)

    if not examples:
        return f"No examples found for type: {task_type}"

    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{question}"),
         ("ai", "{answer}")]
    )
    
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=[{'question': q, 'answer': a} for q, a in examples],
    )

    final_prompt_with_few_shot = ChatPromptTemplate.from_messages(
        [("system", f"Process the message based on {task_type} examples"),
         few_shot_prompt,
         ("human", "{question}")]
    )

    chain_with_few_shot = final_prompt_with_few_shot | chat_model
    chat_ai = chain_with_few_shot.invoke({"question": message})

    return chat_ai.content

def get_response(message, task_type="train"):
    """
    Handles 'sense', 'opposite', and 'custom train' in one function.
    :param message: The input message or question.
    :param task_type: Type of task to handle: 'sense', 'opposite', or 'train' (default).
    :return: Response from the AI model.
    """
    # Define example templates based on task type
    examples = []
    system_message = ""

    if task_type == "sense":
        examples = [
            {"question": "من عاشق این فیلمم!", "answer": "positive"},
            {"question": "از این صندلی خوشم نمی‌اد", "answer": "negative"}
        ]
        system_message = "احساس متن زیر رو دسته بندی کن"
        
    elif task_type == "opposite":
        examples = [
            {"question": "خوشحال", "answer": "ناراحت"},
            {"question": "مادر", "answer": "مهربان"},
            {"question": "روز", "answer": "خورشید"}
        ]
        system_message = "get opposite of word"
    
    elif task_type == "train":
        # Use custom examples provided by user
        global texamples
        if not texamples:
            return "No training examples provided."
        examples = texamples
        system_message = "Provide a response based on training examples."

    # Create example prompt and few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{question}"),
         ("ai", "{answer}")]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    # Final prompt with system message and few-shot examples
    final_prompt_with_few_shot = ChatPromptTemplate.from_messages(
        [("system", system_message),
         few_shot_prompt,
         ("human", "{question}")]
    )

    # Chain the prompt to the AI model and get the response
    chain_with_few_shot = final_prompt_with_few_shot | chat_model
    chat_ai = chain_with_few_shot.invoke({"question": message})

    return chat_ai.content

def chatwithllm(message, topic='default_topic', system='default_system'):
    """
    Run the plasec.py script with the given arguments and system prompt.
    """
    try:
        

        # Run plasec.py with the message, topic, and system prompt
        result = subprocess.run(
            ['python3', 'scripts/plasec.py', message, topic, system],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()  # Return the output from the script
    except Exception as e:
        print(f"Error running script: {str(e)}")
        return f"Error running script: {str(e)}"
@csrf_exempt
def play_in_telegram(request):
    if request.method == 'POST':
        # Replace with your actual bot token and chat ID
        bot_token = "YOUR_TELEGRAM_BOT_TOKEN_BETA"
        chat_id = "108704602"

        # Send the /start command to the Telegram bot
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': '/start'
        }

        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to send command to Telegram'}, status=500)
       
def search_messages(request):
    query = request.GET.get('q')
    results =[]
    if query:
        # Filter messages that contain the query and are not empty
        results = ChatMessage.objects.filter(content__icontains=query).exclude(content="")
        s=[]
        for x in results:
            if x.message :
               s.append(x)
        # Increment score by 1 for each matching message
        for message in s:
            message.score += 1
            message.save()  # Save the updated message instance

    return render(request, 'search_results.html', {'messages': s})

def message_clicked(request, message_id):
    try:
        message = ChatMessage.objects.get(id=message_id)
        message.score += 10  # Increment score by 10 when clicked
        message.save()  # Save the updated message instance
        return JsonResponse({'status': 'success', 'new_score': message.score})
    except ChatMessage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'})
def run_cal_script(a, b, op):
    """
    Run the cal.py script with the given arguments.
    """
    try:
        # Command to run cal.py with the arguments
        result = subprocess.run(
            ['python3', 'scripts/cal.py', str(a), str(b), op],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()  # Return the output from the script
    except Exception as e:
        return f"Error running script: {str(e)}"

def run_hi_script():
    try:
        # Command to run cal.py with the arguments
        result = subprocess.run(
            ['python3', 'scripts/hi.py'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()  # Return the output from the script
    except Exception as e:
        return f"Error running script: {str(e)}"
@csrf_exempt
def delete_message(request, message_id):
    if request.method == 'POST':
        try:
            message = ChatMessage.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'status': 'success'})
        except ChatMessage.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Message not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def chat_view(request):
    global topic
    global system
    try:  
     initialize_db();
    except Exception as e:
      result=f"error creating databse {str(e)}"
    form = ChatMessage()
    messages = ChatMessage.objects.all().order_by('-timestamp')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['message']
            try:
                # Handle "cal" command (e.g., "cal 12 23 sum")
                if user_message.startswith("cal"):
                    tokens = user_message.split()
                    if len(tokens) == 4:
                        # Extract arguments and run cal.py
                        num1 = tokens[1]
                        num2 = tokens[2]
                        operation = tokens[3]
                        result = run_cal_script(num1, num2, operation)
                    else:
                        result = "Invalid format. Use: cal <num1> <num2> <operation>"
                elif user_message.startswith("hi"):
                          
                        result = run_hi_script()
                elif user_message.strip() == "$sense":
                    # Fetch the most recent message
                    previous_message = ChatMessage.objects.last()
                    previous_message=previous_message.message+previous_message.response
                    if previous_message:
                        result =gettrainedmodel(previous_message,"sense")  
                    else:
                        result = "add message after $sense"
                elif user_message.startswith("$sense "):
                    # Analyze the content after "$sense"
                    sense_content = user_message.replace("$sense ", "", 1)
                    result = gettrainedmodel(sense_content,"sense")  
                elif user_message.startswith("$opposite "):
                    # Analyze the content after "$sense"
                    sense_content = user_message.replace("$opposite ", "", 1)
                    result = gettrainedmodel(sense_content,"opposite")   
                   
                elif user_message.startswith("$question "):
                    
                  # Example input: $question happy, sad, opposite, get opposite of word
                  question_content = user_message.replace("$question ", "", 1)
                  try:
                   parts = question_content.split(',')  # Split by commas
                   question = parts[0].strip()
                   answer = parts[1].strip()
                   q_type = parts[2].strip() if len(parts) > 2 else 'general'  # Default type is 'general'
                   system_message = parts[3].strip() if len(parts) > 3 else 'default_system'
                   # Add the new question to the database
                   addexaample(question, answer, q_type, system_message)
                   result = f"Question '{question}' with type '{q_type}' added."
                  except Exception as e:
                     result = f"Error processing question: {str(e)}"
         
                elif user_message.strip() == "$opposite":
                    # Fetch the most recent message
                    previous_message = ChatMessage.objects.last()
                    previous_message=previous_message.message+previous_message.response
                    if previous_message:
                        result =gettrainedmodel(previous_message,"opposite")  # You can replace this with actual sense analysis logic
                    else:
                        result = "add message after $sense"
                   
                elif   user_message.startswith("$chat"):
                   user_message=user_message.replace("$chat","")
                   result=chatwithllm(user_message,topic,system)
                
                elif user_message.startswith("$topic"):
                    user_message = user_message.replace("$topic ", "")
                    topic = user_message
                    last_message = ChatMessage.objects.last()  # Get the last message instance
                    if last_message:
                        last_message.topic = topic  # Update the topic
                        last_message.score += 10  # Increment the score
                        last_message.save()  # Save the updated instance
                    result = "Topic is " + topic
                   
                elif user_message.startswith("$system"):
                    user_message = user_message.replace("$system", "")
                    system = user_message
                    last_message = ChatMessage.objects.last()  # Get the last message instance
                    if last_message:
                        last_message.system = system  # Update the system
                        last_message.score += 10  # Increment the score
                        last_message.save()  # Save the updated instance
                    result = "System is " + system
                
                else:
                    result = "Command not recognized."

            except Exception as e:
                result = f"Error: {str(e)}"
            
            # Save the message and response to the database
            ChatMessage.objects.create(
                message=user_message,
                response=result,
                timestamp=timezone.now(),
                topic=topic, 
                system=system,
                score=0,
            )

    return render(request, 'chatapp/chat.html', {'form': form, 'messages': messages})
