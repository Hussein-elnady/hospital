# admission/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/create/', views.patient_registration, name='patient_registration'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('generate_reports/', views.generate_reports, name='generate_reports'),
    path('search/', views.search_patient, name='search_patient'),
    path('success/', views.success_view, name='success_view'),
    path('patient/<int:pk>/preview/', views.print_preview, name='print_preview'),


]
