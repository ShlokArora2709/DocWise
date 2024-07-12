from django.db import models
from  Login.models import CustomUser

class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=CustomUser.objects.first().get_username())
    report = models.FileField()
    summary = models.TextField()
    dictionary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)