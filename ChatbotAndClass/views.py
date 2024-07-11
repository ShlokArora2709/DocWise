from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as GenAI
import os
import re

load_dotenv()

GenAI.configure(api_key=os.getenv('GEMINI_API_KEY'))

llm=GenAI.GenerativeModel('gemini-1.5-pro')

def generate_response(user_input):

    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    response = llm.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    cleaned_response = re.sub(r'\*\*(.*?)\*\*', r'\1',response.text.strip())
    return cleaned_response


def chatbot(request):
    if "conversation" not in request.POST:
        conversation=""
    else:
         conversation=request.POST["conversation"]

    userinput=""
    if request.method=="POST":
        userinput=request.POST["userinput"]
        conversation+=f"User: {userinput}\n"
        response=generate_response(conversation)
        conversation += f"\nChatbot: {response}"
    
    return render(request, 'chatbot.html', {'conversation': conversation, 'userinput': userinput})