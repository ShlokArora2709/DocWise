from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Doctor

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['username', 'email', 'password1', 'password2', 'license_file']

    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    license_file = forms.FileField(label='License File', help_text='Upload your doctor license (JPEG, PNG, PDF)')