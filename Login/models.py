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
