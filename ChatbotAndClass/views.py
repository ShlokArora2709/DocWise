from django.shortcuts import render,redirect
from dotenv import load_dotenv
import google.generativeai as GenAI
import os
import re
from .froms import UploadFileForm
from pypdf import PdfReader
from django.contrib.auth.decorators import login_required
from simplegmail import Gmail
gmail=Gmail()

load_dotenv()
GenAI.configure(api_key=os.getenv('GEMINI_API_KEY'))
llm=GenAI.GenerativeModel('gemini-1.5-pro')

input_text=f'''Generate a summary report of the patient\'s medical report and make a dictionary
 for the things that were checked in the medical report. The report dictionary should have 
 items like RBC, urea, etc., that are mentioned in the report. Your output should be like 
 this:**Summary:**The patient, a 45-year-old female, presents with elevated creatinine 
 levels (2.88 mg/dL) indicating decreased kidney function (GFR of 19.90 ml/min/1.73m), 
 categorized as stage G4 chronic kidney disease. Her urea levels are also significantly 
 elevated (53.64 mg/dL) alongside high uric acid (8.62 mg/dL), suggesting impaired waste 
 excretion by the kidney
 
 report_dict =
 ["Hemoglobin": 13.50,"Packed Cell Volume (PCV)": 41.40,"RBC Count": 4.60,"MCV": 90.00,
  "MCH": 29.30,"MCHC": 32.60,"Red Cell Distribution Width (RDW)": 20.20,
  "Total Leukocyte Count (TLC)": 6.10,"Segmented Neutrophils": 68.30,"Lymphocytes": 23.00,
  "Urine Proteins": "Present 2+","Urine Glucose": "Nil","Urine Ketones": "Nil",
  "Urine Bilirubin": "Nil","Urine Urobilinogen": "Normal",
  "Urine Leucocyte Esterase": "Present 1+","Urine Nitrite": "Negative","Urine RBC": "Nil",
  "Urine Pus Cells": "6-8","Urine Epithelial Cells": "1-2","Urine Casts": "Nil",
  "Urine Crystals": "Nil","Urine Others": "Nil"]'''
def generate_response(user_input,llm):

    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    response = llm.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    cleaned_response = re.sub(r'\*\*(.*?)\*\*', r'\1',response.text.strip())
    return cleaned_response


def send_email(request,doc_mail,meet_link):
    user = request.user
    if user.is_authenticated:
        params = {
            "to": doc_mail,
            "sender":"docwise.shlokarora@gmail.com" ,
            "cc":user.email,
            "bcc":"shlokarora2709@gmail.com",
            "subject": "Appoeintment Confirmation",
            "msg_html": f"Hello Doctor, {user.username} has booked an appointment with you. Please check your schedule and confirm the appointment. Here is the link to the meeting: {meet_link}",
            }
        gmail.send_message(**params)
        return redirect('home')
    

def chatbot(request):
    if "conversation" not in request.POST:
        conversation=""
    else:
         conversation=request.POST["conversation"]

    userinput=""
    if request.method=="POST":
        userinput=request.POST["userinput"]
        conversation+=f"User: {userinput}\n"
        response=generate_response(conversation,llm)
        conversation += f"\nChatbot: {response}"
    
    return render(request, 'chatbot.html', {'conversation': conversation, 'userinput': userinput})


@login_required
def upload_report(request):
    file_text = ""
    response = ""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            reader = PdfReader(file)
            for i in range(len(reader.pages)):  
                page = reader.pages[i]
                file_text += page.extract_text()
            response = llm.generate_content(f"{input_text} {file_text}")
            response=response.text.strip()
            summary_start = response.find("**Summary:**") + len("**Summary:**")
            dict_start = response.find("**report_dict =**")
            summary = response[summary_start:dict_start].strip()
            dict_report_start = response.find("{", dict_start)
            dict_report_end = response.rfind("}") + 1
            dict_report = response[dict_report_start:dict_report_end].strip()

            os.remove(file.name)
            return redirect('home')
        
    return render(request, 'upload_report.html')
