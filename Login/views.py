from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DoctorRegistrationForm
from ChatbotAndClass.models import Report

def signup_view(request):
    error = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            error = form.errors.as_text()
            print(error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form, 'error': error})

def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user= authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            error = form.errors.as_text()
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form,'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    if request.user.is_authenticated:
        reports = Report.objects.filter(username=request.user.username)
    else:
        reports = None
    return render(request, 'home.html', {'reports': reports})

def doctor_registration_view(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            error="Doctor registered successfully"
            return redirect('login')
        else:
            error=form.errors.as_text()
    else:
        form = DoctorRegistrationForm()
        error=None
    return render(request, 'doctor_registration.html', {'form': form ,'error': error})