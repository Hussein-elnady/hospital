from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Patient
from .forms import PatientForm
from django.utils import timezone
from django.core.exceptions import ValidationError


# Date and time functionality
from datetime import date, datetime, timedelta
from django.db.models import Count, Avg, Max, Min
from dateutil.relativedelta import relativedelta
from django.db.models import Q


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
def patient_registration(request):
    if request.method == 'POST':
        # Extract data from POST request
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        national_number = request.POST.get('national_number')
        insurance_number = request.POST.get('insurance_number')
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

        # Calculate length of stay if discharge information is available
        discharge_date = request.POST.get('discharge_date')
        discharge_time = request.POST.get('discharge_time')

        # Calculate length of stay if discharge information is available

        length_of_stay = None
        if discharge_date and discharge_time and admission_date and admission_time:
            try:
                admission_date_obj = timezone.datetime.strptime(admission_date, '%Y-%m-%d').date()
                discharge_date_obj = timezone.datetime.strptime(discharge_date, '%Y-%m-%d').date()
                length_of_stay = (discharge_date_obj - admission_date_obj).days
            except ValueError:
                raise ValidationError('Invalid date format for discharge date or admission date')
        else:
            # If discharge information is not available, set length_of_stay to None
            length_of_stay = None

        # Calculate age
        if date_of_birth:
            date_of_birth_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = timezone.now()
            age = relativedelta(today, date_of_birth_obj).years
        else:
            age = None

        # Get the time of registration
        time_of_registration = timezone.now()

        # Get the last admission number
        last_admission_number = Patient.objects.aggregate(Max('admission_number'))['admission_number__max']
        if last_admission_number:
            last_admission_number_str = str(last_admission_number)
            serial_number = int(last_admission_number_str.split('-')[-1]) + 1
            new_admission_number = f"{serial_number:04d}"
        else:
            new_admission_number = "0001"

        # Assign new admission number to the patient
        Patient.admission_number = new_admission_number

        # Create the Patient instance with the extracted data
        patient = Patient(
            full_name=full_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            national_number=national_number,
            insurance_number=insurance_number,
            admission_number=new_admission_number,
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
            time_of_registration=time_of_registration
        )

        # Save the patient object
        patient.save()

        # Store patient ID in session for later use
        request.session['patient_id'] = patient.pk

        return render(request, 'admission/success.html')

    return render(request, 'admission/patient_form.html')


@login_required
def success_view(request):
    # Redirect to main page after displaying success message
    return redirect('main_page')


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'admission/patient_form.html', {'form': form})


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'admission/patient_list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'admission/patient_detail.html', {'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'admission/patient_confirm_delete.html', {'patient': patient})


@login_required
def main_page(request):
    # Retrieve last 5 admitted patients
    recent_admitted_patients = Patient.objects.filter(
        Q(discharge_date__isnull=True) | Q(length_of_stay__isnull=True)
    ).order_by('-admission_date')[:5]

    # Retrieve last 5 discharged patients
    recent_discharged_patients = Patient.objects.exclude(
        Q(discharge_date__isnull=True) | Q(length_of_stay__isnull=True)
    ).order_by('-discharge_date')[:5]

    return render(request, 'admission/main.html', {
        'recent_admitted_patients': recent_admitted_patients,
        'recent_discharged_patients': recent_discharged_patients
    })


@login_required
def generate_reports(request):
    # Retrieve data based on user-selected filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    patients = Patient.objects.filter(admission_date__range=[start_date, end_date])

    # Calculate additional statistics
    total_patients = patients.count()
    male_patients = patients.filter(gender='Male').count()
    female_patients = patients.filter(gender='Female').count()

    # Diagnosis Distribution
    initial_diagnosis_distribution = patients.values('initial_diagnosis').annotate(count=Count('initial_diagnosis'))

    # Length of Stay Analysis
    average_length_of_stay = patients.aggregate(average_length=Avg('length_of_stay'),
                                                min_length=Min('length_of_stay'),
                                                max_length=Max('length_of_stay'))

    # Readmission Rates (Example: within 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    readmitted_patients = patients.filter(discharge_date__gte=thirty_days_ago).exclude(previous_admission=None)
    readmission_rate = (readmitted_patients.count() / total_patients) * 100 if total_patients != 0 else 0

    # Demographic Breakdown
    today = date.today()
    age_groups = {
        '0-18': patients.filter(date_of_birth__gte=today.replace(year=today.year - 18)).count(),
        '19-35': patients.filter(
            date_of_birth__range=(today.replace(year=today.year - 35), today.replace(year=today.year - 19))).count(),
        '36-50': patients.filter(
            date_of_birth__range=(today.replace(year=today.year - 50), today.replace(year=today.year - 36))).count(),
        '51+': patients.filter(date_of_birth__lt=today.replace(year=today.year - 51)).count(),
    }

    # Insurance Coverage Analysis
    insurance_coverage = patients.exclude(insurance_number='').count()
    uninsured_patients = total_patients - insurance_coverage

    # Admission Department Analysis
    admission_departments = patients.values('admission_department').annotate(count=Count('admission_department'))

    # Room Grade Utilization
    room_grade_utilization = patients.values('room_grade').annotate(count=Count('room_grade'))

    # Discharge Status Distribution
    discharge_statuses = patients.values('discharge_status').annotate(count=Count('discharge_status'))

    # Service Type Breakdown
    service_types = patients.values('service_type').annotate(count=Count('service_type'))

    # Operation Procedures Analysis
    operation_procedures = patients.values('operation_procedures').annotate(count=Count('operation_procedures'))

    # Autopsy Rate Calculation
    autopsy_rate = (patients.filter(autopsy=True).count() / total_patients) * 100 if total_patients != 0 else 0

    # Geographical Analysis
    geographical_distribution = patients.values('governorate').annotate(count=Count('governorate'))

    return render(request, 'admission/generate_reports.html', {
        'total_patients': total_patients,
        'male_patients': male_patients,
        'female_patients': female_patients,
        'initial_diagnosis_distribution': initial_diagnosis_distribution,
        'average_length_of_stay': average_length_of_stay,
        'readmission_rate': readmission_rate,
        'age_groups': age_groups,
        'insurance_coverage': insurance_coverage,
        'uninsured_patients': uninsured_patients,
        'admission_departments': admission_departments,
        'room_grade_utilization': room_grade_utilization,
        'discharge_statuses': discharge_statuses,
        'service_types': service_types,
        'operation_procedures': operation_procedures,
        'autopsy_rate': autopsy_rate,
        'geographical_distribution': geographical_distribution,
        'patients': patients,
    })


@login_required
def search_patient(request):
    query = request.GET.get('query', '')

    patients = Patient.objects.filter(full_name__icontains=query)  # Example: Search patients by name

    return render(request, 'admission/search_patient.html', {'patients': patients, 'query': query})


@login_required
def print_preview(request, pk):
    # Fetch data for a specific patient from the database
    patient = get_object_or_404(Patient, pk=pk)

    return render(request, 'admission/print_preview.html', {'patient': patient})
