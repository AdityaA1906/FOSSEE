from django.db import models
from django.contrib.auth.models import User
import json


class DatasetHistory(models.Model):
    """Stores complete dataset history with CSV file and summary statistics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset_history')
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    summary_data = models.JSONField(default=dict, blank=True)
    original_csv = models.FileField(upload_to='datasets/', null=True, blank=True)
    row_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name_plural = 'Dataset Histories'
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_summary_display(self):
        if self.summary_data:
            return f"Total: {self.summary_data.get('total_count', 0)} units"
        return "No summary available"


class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0)
    dataset = models.ForeignKey(DatasetHistory, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploads')

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Upload Histories'

    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentData(models.Model):
    upload = models.ForeignKey(UploadHistory, on_delete=models.CASCADE, related_name='equipment')
    dataset = models.ForeignKey(DatasetHistory, on_delete=models.CASCADE, related_name='equipment_data', null=True, blank=True)
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
