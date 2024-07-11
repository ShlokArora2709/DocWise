from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Customize the admin interface if needed
    pass

# Register your CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)