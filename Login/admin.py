from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Doctor

class CustomUserAdmin(UserAdmin):
    # Customize the admin interface if needed
    pass

# Register your CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)


class DoctorAdmin(admin.ModelAdmin):
    list_filter = ('is_approved',)
    actions = ['approve_doctors']

    def approve_doctors(self, request, queryset):
        queryset.update(is_approved=True)
    approve_doctors.short_description = "Approve selected doctors"

admin.site.register(Doctor, DoctorAdmin)