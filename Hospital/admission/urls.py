# admission/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('main_page/', views.main_page, name='main_page'),
    # path('', views.patient_list, name='patient_list'),
    path('patients/', views.patient_list, name='patient_list'),
    path('admissions/', views.admission_list, name='admission_list'),
    path('discharges/', views.discharge_list, name='discharge_list'),
    path('patient/create/', views.patient_create, name='patient_create'),
    path('admission/create/<int:patient_pk>/', views.admission_create, name='admission_create'),    
    path('admission/discharge/create/<int:admission_pk>/', views.discharge_create, name='discharge_create'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('success/<int:patient_pk>/', views.success, name='success'),
    path('admission/<int:pk>/', views.admission_detail, name='admission_detail'),   
    path('admission/<int:pk>/edit/', views.admission_edit, name='admission_edit'),
    path('admission/<int:pk>/delete/', views.admission_delete, name='admission_delete'),
    path('discharge/delete/<int:admission_pk>/', views.discharge_delete, name='discharge_delete'),
    path('discharge/list/', views.discharge_list, name='discharge_list'),
    path('discharge/edit/<int:admission_pk>/', views.discharge_edit, name='discharge_edit'),


]
