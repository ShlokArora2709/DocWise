from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'custom_user'

    # Specify unique related_name for groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Unique related_name for groups
        blank=True,
        help_text='The groups this user belongs to.',
    )

    # Specify unique related_name for user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Unique related_name for user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
    )

    is_doctor = models.BooleanField(default=False)

class Doctor(models.Model):
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
    username = models.CharField(max_length=150,default='Doctor')
    email = models.EmailField(unique=True, default='example@gmail.com')
    license_file = models.FileField(upload_to='licenses/',default=r"C:\Users\Shlok\Pictures\Screenshots\Screenshot (20).png")
    speciality = models.CharField(max_length=150,choices=speciality_CHOICES, default='General Physician')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def isApproved(self):
        return self.is_approved
    
    is_doctor = models.BooleanField(default=False)

# @receiver(post_save, sender=Doctor)
# def create_user(sender, instance, created, **kwargs):
#     if created:
#         CustomUser.objects.create(username=instance.username,email=instance.email,password=instance.password,is_doctor=True)
