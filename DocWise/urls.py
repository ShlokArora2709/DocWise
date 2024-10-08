"""
URL configuration for DocWise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Login.views import *
from django.conf import settings
from django.conf.urls.static import static
from ChatbotAndClass.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('chatbot/', chatbot, name='chatbot'),
    path('chatbot_response/', chatbot_response, name='chatbot_response'),
    path('upload_report/', upload_report, name='upload_report'),
    path('signup/doctor/', doctor_registration_view, name='doctor_registration'),
    path('search/', search_doctors, name='search_doctors'),
    path('make_appointment/', make_appointment, name='make_appointment'),
    path('videocall/<str:room_id>/', video_call, name='video_call'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
