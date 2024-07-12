from django.contrib import admin
from .models import CustomUser, Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()