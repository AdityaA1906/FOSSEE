from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('auth/google/', views.google_login, name='google-login'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('data/', views.get_equipment_data, name='get-data'),
    path('stats/', views.get_statistics, name='get-stats'),
    path('history/', views.get_upload_history, name='get-history'),
    path('history/<int:pk>/', views.get_dataset_details, name='dataset-details'),
    path('generate-pdf/', views.generate_pdf_report, name='generate-pdf'),
]
