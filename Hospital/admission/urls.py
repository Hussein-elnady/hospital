# admission/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_home, name='admission_home'),  # Define a URL pattern for admission home
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('success/', views.success_view, name='success_url'),
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('search/', views.search_patient, name='search_patient'),
]
