from django.db import models
from  Login.models import CustomUser

class Report(models.Model):
    username = models.CharField(max_length=150)  
    report = models.FileField()
    summary = models.TextField()
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
