# views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import PatientForm
from .models import Patient
import datetime

from lib.national_id import NationalID


@login_required
def patient_registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        national_number = request.POST.get('national_number')
        insurance_number = request.POST.get('insurance_number')
        admission_number = request.POST.get('admission_number')
        social_status = request.POST.get('social_status')
        religion = request.POST.get('religion')
        profession = request.POST.get('profession')
        employer = request.POST.get('employer')
        address = request.POST.get('address')
        city_village = request.POST.get('city_village')
        governorate = request.POST.get('governorate')
        phone_number = request.POST.get('phone_number')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        emergency_contact_address = request.POST.get('emergency_contact_address')
        emergency_contact_phone_number = request.POST.get('emergency_contact_phone_number')
        insurance_provider_contact_name = request.POST.get('insurance_provider_contact_name')
        insurance_provider_relationship = request.POST.get('insurance_provider_relationship')
        insurance_provider_address = request.POST.get('insurance_provider_address')
        insurance_provider_phone_number = request.POST.get('insurance_provider_phone_number')
        admitted_by = request.POST.get('admitted_by')
        accident_location = request.POST.get('accident_location')
        police_report = request.POST.get('police_report')
        previous_admission = request.POST.get('previous_admission')
        treating_physician = request.POST.get('treating_physician')
        admission_department = request.POST.get('admission_department')
        room = request.POST.get('room')
        room_grade = request.POST.get('room_grade')
        initial_diagnosis = request.POST.get('initial_diagnosis')
        admission_date = request.POST.get('admission_date')
        admission_time = request.POST.get('admission_time')
        discharge_date = request.POST.get('discharge_date')
        discharge_time = request.POST.get('discharge_time')
        length_of_stay = request.POST.get('length_of_stay')
        final_diagnosis = request.POST.get('final_diagnosis')
        associated_diagnosis = request.POST.get('associated_diagnosis')
        service_type = request.POST.get('service_type')
        operation_procedures = request.POST.get('operation_procedures')
        autopsy = request.POST.get('autopsy')
        discharge_status = request.POST.get('discharge_status')
        discharge_destination = request.POST.get('discharge_destination')

        patient = Patient(full_name=full_name,
                          date_of_birth=date_of_birth,
                          gender=gender,
                          national_number=national_number,
                          insurance_number=insurance_number,
                          admission_number=admission_number,
                          social_status=social_status,
                          religion=religion,
                          profession=profession,
                          employer=employer,
                          address=address,
                          city_village=city_village,
                          governorate=governorate,
                          phone_number=phone_number,
                          emergency_contact_name=emergency_contact_name,
                          emergency_contact_relationship=emergency_contact_relationship,
                          emergency_contact_address=emergency_contact_address,
                          emergency_contact_phone_number=emergency_contact_phone_number,
                          insurance_provider_contact_name=insurance_provider_contact_name,
                          insurance_provider_relationship=insurance_provider_relationship,
                          insurance_provider_address=insurance_provider_address,
                          insurance_provider_phone_number=insurance_provider_phone_number,
                          admitted_by=admitted_by,
                          accident_location=accident_location,
                          police_report=police_report,
                          previous_admission=previous_admission,
                          treating_physician=treating_physician,
                          admission_department=admission_department,
                          room=room,
                          room_grade=room_grade,
                          initial_diagnosis=initial_diagnosis,
                          admission_date=admission_date,
                          admission_time=admission_time,
                          discharge_date=discharge_date,
                          discharge_time=discharge_time,
                          length_of_stay=length_of_stay,
                          final_diagnosis=final_diagnosis,
                          associated_diagnosis=associated_diagnosis,
                          service_type=service_type,
                          operation_procedures=operation_procedures,
                          autopsy=autopsy,
                          discharge_status=discharge_status,
                          discharge_destination=discharge_destination
                          )

        patient.save()
        return render(request, 'admission/success.html')
    return render(request, 'admission/pt_register.html')


def success_view(request):
    return render(request, 'admission/success.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            error_message = "Invalid username or password."
            return render(request, 'admission/login.html', {'error_message': error_message})
    return render(request, 'admission/login.html')


@login_required
def main_page(request):
    if request.user.is_superuser:  # Check if user is admin
        return render(request, 'admission/main.html', {'admin': True})
    else:
        return render(request, 'admission/main.html', {'admin': False})


def admission_home(request):
    return redirect('register_patient')  # Redirect to patient registration page or any other relevant page


@login_required
def record_patient_data(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_patient_success')
    else:
        form = PatientForm()
    return render(request, 'admission/record_patient_form.html', {'form': form})


@login_required
def generate_reports(request):
    patients = Patient.objects.all()  # Example: Fetch all patients from the database

    return render(request, 'admission/generate_reports.html', {'patients': patients})


@login_required
def search_patient(request):
    query = request.GET.get('query', '')

    patients = Patient.objects.filter(full_name__icontains=query)  # Example: Search patients by name

    return render(request, 'admission/search_patient.html', {'patients': patients, 'query': query})
