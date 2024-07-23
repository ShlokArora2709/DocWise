from django.contrib import admin
from .models import CustomUser, Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('username', 'summary', 'created_at')
    search_fields = ('summary', 'dictionary')
    date_hierarchy = 'created_at'