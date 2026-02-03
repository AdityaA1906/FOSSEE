from django.contrib import admin
from .models import EquipmentData, UploadHistory

@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'created_at']
    list_filter = ['equipment_type', 'created_at']
    search_fields = ['equipment_name', 'equipment_type']

@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'row_count']
    list_filter = ['uploaded_at']
    search_fields = ['filename']
