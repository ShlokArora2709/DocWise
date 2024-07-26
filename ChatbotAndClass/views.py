from django.shortcuts import render,redirect
from dotenv import load_dotenv
import google.generativeai as GenAI
import os
import re
from .froms import UploadFileForm
from pypdf import PdfReader
from django.contrib.auth.decorators import login_required
from simplegmail import Gmail
from django.http import JsonResponse
from Login.models import Doctor
from django.contrib import messages
import uuid
from .models import Report
from django.contrib.messages import get_messages

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


speciality_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Pediatrics', 'Pediatrics'),
        ('Radiology', 'Radiology'),
        ('Oncology', 'Oncology'),
        ('Gastroenterology', 'Gastroenterology'),
        ('Hematology', 'Hematology'),
        ('Endocrinology', 'Endocrinology'),
        ('Nephrology', 'Nephrology'),
        ('Pulmonology', 'Pulmonology'),
        ('Urology', 'Urology'),
        ('Orthopedics', 'Orthopedics'),
        ('Rheumatology', 'Rheumatology'),
        ('Infectious Disease', 'Infectious Disease'),
        ('Allergy and Immunology', 'Allergy and Immunology'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Pathology', 'Pathology'),
        ('Psychiatry', 'Psychiatry'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
        ('Plastic Surgery', 'Plastic Surgery'),
        ('General Surgery', 'General Surgery'),
        ('Thoracic Surgery', 'Thoracic Surgery'),
        ('Vascular Surgery', 'Vascular Surgery'),
        ('Neurosurgery', 'Neurosurgery'),
        ('Pediatric Surgery', 'Pediatric Surgery'),
        ('Trauma Surgery', 'Trauma Surgery'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('Family Medicine', 'Family Medicine')
    ]

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
            "cc":[user.email],
#            "bcc":[],
            "subject": "Appointment Confirmation",
            "msg_html": f"Hello Doctor, {user.username} has booked an appointment with you. Please check your schedule and confirm the appointment. Here is the link to the meeting: {meet_link}",
            }
        gmail.send_message(**params)
        return redirect('home')
    

def chatbot(request): 
    conversation_history = request.session.get('conversation_history', [])  
    return render(request, 'chatbot.html', {'conversation_history': conversation_history})


def chatbot_response(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_input = request.GET.get('user_input', '')
        conversation = request.session.get('conversation', [])
        conversation.append({'type': 'user', 'message': user_input})
        full_context = " ".join([msg['message'] for msg in conversation])
        response = generate_response(full_context, llm)
        conversation.append({'type': 'bot', 'message': response})
        request.session['conversation'] = conversation
        return JsonResponse({"response": response})
    return JsonResponse({"response": "Invalid request"})

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
            Report.objects.create(username=request.user, report=file, summary=summary, data=dict_report)

            messages.success(request, "Report uploaded and saved successfully!")
            return redirect('upload_report')
        
    storage = get_messages(request)
    messages_list = []
    for message in storage:
        messages_list.append({
            'level': message.level,
            'message': message.message,
            'tags': message.tags
        })

    context = {
        'file_text': file_text,
        'messages': messages_list
    }

    return render(request, 'upload_report.html', context)

@login_required
def search_doctors(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        speciality = request.GET.get('speciality', '')
        doctors = Doctor.objects.filter(username__icontains=query, speciality__icontains=speciality, is_approved=True)
        results = [
            {
                "username": doctor.username,
                "email": doctor.email,
                "speciality": doctor.speciality,
            } for doctor in doctors
        ]
        return JsonResponse({"results": results})
    return render(request, 'search_doctors.html', {'speciality_CHOICES': speciality_CHOICES})

@login_required
def make_appointment(request):
    if request.method == "POST":
        doc_mail = request.POST["DocMail"]
        meet_link =f"http://127.0.0.1:8000/videocall/{uuid.uuid4()}"
        send_email(request,doc_mail,meet_link)
    return JsonResponse({"message": "Appointment booked successfully!"})

@login_required
def video_call(request, room_id):
    return render(request, 'VideoCall.html', {'room_id': room_id})