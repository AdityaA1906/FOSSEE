from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EquipmentData, UploadHistory, DatasetHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = '__all__'


class UploadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadHistory
        fields = ['id', 'filename', 'uploaded_at', 'row_count']


class DatasetHistorySerializer(serializers.ModelSerializer):
    summary_display = serializers.CharField(source='get_summary_display', read_only=True)
    
    class Meta:
        model = DatasetHistory
        fields = ['id', 'filename', 'upload_date', 'summary_data', 'original_csv', 'row_count', 'summary_display']
