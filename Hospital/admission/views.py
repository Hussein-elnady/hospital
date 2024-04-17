from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient, Admission, Discharge
from .forms import PatientForm, AdmissionForm, DischargeForm
from django.utils import timezone


# ---------------------------------------- Login_View ---------------------------------------- #

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


# ---------------------------------------- Main_Page ---------------------------------------- #

@login_required
def main_page(request):
    # Retrieve recently admitted patients
    admitted_patients = Admission.objects.filter(discharge__isnull=True).order_by('-admission_date')

    # Retrieve recently discharged patients
    discharged_patients = Discharge.objects.order_by('-admission_number')[:10]

    context = {
        'admitted_patients': admitted_patients,
        'discharged_patients': discharged_patients,
    }

    return render(request, 'admission/main.html', context)


# ---------------------------------------- Patient ---------------------------------------- #
@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            national_number = form.cleaned_data['national_number']
            if Patient.objects.filter(national_number=national_number).exists():
                error_message = 'A patient with the same national number already exists.'
            else:
                patient = form.save()
                print("Patient saved successfully:", patient)  # Debugging statement
                return redirect('success', patient_pk=patient.pk)
        else:
            print("Form errors:", form.errors)  # Debugging statement
            error_message = 'A patient with the same national number already exists.'
    else:
        form = PatientForm()
        error_message = None  # Initialize error_message variable for GET requests

    return render(request, 'admission/patient_create.html', {'form': form, 'error_message': error_message})


@login_required
def success(request, patient_pk):
    patient = Patient.objects.get(pk=patient_pk)
    return render(request, 'admission/success.html', {'patient': patient})


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('main_page', pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'admission/patient_edit.html', {'form': form, 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('main_page')  # Assuming 'home' is the URL name for the main page
    return render(request, 'admission/patient_confirm_delete.html', {'patient': patient})


@login_required
def patient_list(request):
    search_national_number = request.GET.get('search_national_number')

    if search_national_number:
        patients = Patient.objects.filter(national_number__icontains=search_national_number).order_by('full_name')
    else:
        patients = Patient.objects.all().order_by('full_name')

    return render(request, 'admission/patient_list.html', {'patients': patients})


# ---------------------------------------- Admission ---------------------------------------- #

@login_required
def admission_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.patient = patient
            admission.save()
            messages.success(request, 'Admission created successfully!')
            return redirect('admission_detail', pk=admission.pk)  # Redirect to 'admission_detail'
    else:
        form = AdmissionForm()
    return render(request, 'admission/admission_create.html', {'form': form, 'patient': patient})


@login_required
def admission_edit(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=admission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admission updated successfully!')
            return redirect('main_page')  # Redirect to 'main_page'
    else:
        form = AdmissionForm(instance=admission)
    return render(request, 'admission/admission_edit.html', {'form': form, 'admission': admission})


@login_required
def admission_delete(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        admission.delete()
        messages.success(request, 'Admission deleted successfully!')
        return redirect('main_page')  # Redirect to the main page or any other appropriate page
    return render(request, 'admission/admission_confirm_delete.html', {'admission': admission})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    admissions = patient.admissions.all()
    return render(request, 'admission/patient_detail.html', {'patient': patient, 'admissions': admissions})


@login_required
def admission_detail(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    context = {'admission': admission}
    return render(request, 'admission/admission_detail.html', context)


# ---------------------------------------- Discharge ---------------------------------------- #

def discharge_create(request, admission_pk):
    admission = get_object_or_404(Admission, pk=admission_pk)
    patient_name = admission.patient.full_name  # Get the patient's name from the admission
    if request.method == 'POST':
        form = DischargeForm(request.POST)
        if form.is_valid():
            discharge = form.save(commit=False)
            discharge.admission_number = admission  # Assign admission object directly
            discharge.save()
            messages.success(request, 'Discharge information added successfully.')
            return redirect('admission_detail', pk=admission.pk)
    else:
        form = DischargeForm(initial={'admission_number': admission.admission_number})
    return render(request, 'admission/discharge_form.html', {'form': form, 'patient_name': patient_name})


@login_required
def admission_list(request):
    admissions = Admission.objects.all()
    return render(request, 'admission/admission_list.html', {'admissions': admissions})


@login_required
def discharge_list(request):
    discharges = Discharge.objects.all()
    return render(request, 'admission/discharge_list.html', {'discharges': discharges})


@login_required
def discharge_edit(request, admission_pk):
    admission = get_object_or_404(Admission, pk=admission_pk)
    discharge_instance, created = Discharge.objects.get_or_create(admission_number=admission)
    form = DischargeForm(request.POST or None, instance=discharge_instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Discharge details updated successfully!')
        return redirect('admission_detail', pk=admission_pk)

    context = {
        'admission': admission,
        'form': form,
    }
    return render(request, 'admission/discharge_edit.html', context)


@login_required
def discharge_delete(request, admission_pk):
    admission = get_object_or_404(Admission, pk=admission_pk)
    discharge_instance = get_object_or_404(Discharge, admission_number=admission)
    if request.method == 'POST':
        discharge_instance.delete()
        messages.success(request, 'Discharge details deleted successfully!')
        return redirect('main_page')
    return render(request, 'admission/discharge_confirm_delete.html', {'admission': admission})
