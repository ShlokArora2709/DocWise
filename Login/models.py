from django.db import models

from django.contrib.auth.models import AbstractUser
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
    username = models.CharField(max_length=150,default='Doctor')
    email = models.EmailField(unique=True, default='example@gmail.com')
    password = models.CharField(max_length=128,default='12345')  # Use Django's built-in auth system for passwords
    license_file = models.FileField(upload_to='licenses/',default=r"C:\Users\Shlok\Pictures\Screenshots\Screenshot (20).png")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'