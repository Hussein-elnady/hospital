from django import forms
from .models import Patient, Admission, Discharge
from datetime import datetime


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['national_number', 'full_name', 'insurance_number', 'social_status', 'religion',
                  'profession', 'employer', 'address', 'city_village', 'governorate', 'phone_number']
        widgets = {
            'national_number': forms.TextInput(attrs={'placeholder': 'Enter National Number'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter Age'}),
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            'insurance_number': forms.TextInput(attrs={'placeholder': 'Enter Insurance Number'}),
            'social_status': forms.Select(attrs={'placeholder': 'Select Social Status'}),
            'religion': forms.Select(attrs={'placeholder': 'Select Religion'}),
            'profession': forms.TextInput(attrs={'placeholder': 'Enter Profession'}),
            'employer': forms.TextInput(attrs={'placeholder': 'Enter Employer'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Address'}),
            'city_village': forms.TextInput(attrs={'placeholder': 'Enter City/Village'}),
            'governorate': forms.TextInput(attrs={'placeholder': 'Enter Governorate'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
        }
        labels = {
            'national_number': 'National Number',
            'full_name': 'Full Name',
            'date_of_birth': 'Date of Birth',
            'age': 'Age',
            'gender': 'Gender',
            'insurance_number': 'Insurance Number',
            'social_status': 'Social Status',
            'religion': 'Religion',
            'profession': 'Profession',
            'employer': 'Employer',
            'address': 'Address',
            'city_village': 'City/Village',
            'governorate': 'Governorate',
            'phone_number': 'Phone Number',
        }
        help_texts = {
            'national_number': 'Enter your national number (14 digits)',
            'date_of_birth': 'Enter your date of birth in YYYY-MM-DD format',
            'age': 'Enter your age',
            'insurance_number': 'Enter your insurance number',
            'phone_number': 'Enter your phone number',
        }

    def clean_national_number(self):
        national_number = self.cleaned_data['national_number']
        if national_number:
            # Perform more thorough national ID validation here (optional)
            pass
        return national_number


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = '__all__'
        widgets = {
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Name'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'placeholder': 'Enter Relationship'}),
            'emergency_contact_address': forms.TextInput(attrs={'placeholder': 'Enter Address'}),
            'emergency_contact_phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'insurance_provider_contact_name': forms.TextInput(attrs={'placeholder': 'Enter Contact Name'}),
            'insurance_provider_relationship': forms.TextInput(attrs={'placeholder': 'Enter Relationship'}),
            'insurance_provider_address': forms.TextInput(attrs={'placeholder': 'Enter Address'}),
            'insurance_provider_phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'treating_physician': forms.TextInput(attrs={'placeholder': 'Enter Treating Physician'}),
            'admission_department': forms.TextInput(attrs={'placeholder': 'Enter Department'}),
            'room': forms.TextInput(attrs={'placeholder': 'Enter Room'}),
            'room_grade': forms.TextInput(attrs={'placeholder': 'Enter Room Grade'}),
            'initial_diagnosis': forms.Textarea(attrs={'placeholder': 'Enter Initial Diagnosis'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'admission_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_relationship': 'Relationship',
            'emergency_contact_address': 'Address',
            'emergency_contact_phone_number': 'Phone Number',
            'insurance_provider_contact_name': 'Insurance Contact Name',
            'insurance_provider_relationship': 'Relationship',
            'insurance_provider_address': 'Address',
            'insurance_provider_phone_number': 'Phone Number',
            'admitted_by': 'Admitted By',
            'accident_location': 'Accident Location',
            'police_report': 'Police Report',
            'previous_admission': 'Previous Admission',
            'treating_physician': 'Treating Physician',
            'admission_department': 'Department',
            'room': 'Room',
            'room_grade': 'Room Grade',
            'initial_diagnosis': 'Initial Diagnosis',
            'admission_date': 'Admission Date',
            'admission_time': 'Admission Time',
        }
        help_texts = {
            'emergency_contact_phone_number': 'Enter emergency contact phone number',
            'insurance_provider_phone_number': 'Enter insurance provider phone number',
            'admission_date': 'Enter admission date in YYYY-MM-DD format',
            'admission_time': 'Enter admission time in HH:MM:SS format',
        }


class DischargeForm(forms.ModelForm):
    class Meta:
        model = Discharge
        fields = '__all__'
        widgets = {
            'admission_number': forms.TextInput(attrs={'readonly': True}),
            'discharge_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter Discharge Date'}),
            'discharge_time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Enter Discharge Time'}),
            'length_of_stay': forms.NumberInput(attrs={'placeholder': 'Length of Stay (days)'}),
            'final_diagnosis': forms.Textarea(attrs={'placeholder': 'Enter Final Diagnosis'}),
            'associated_diagnosis': forms.Textarea(attrs={'placeholder': 'Enter Associated Diagnosis'}),
            'service_type': forms.Select(attrs={'placeholder': 'Select Service Type'}),
            'operation_procedures': forms.Textarea(attrs={'placeholder': 'Enter Operation Procedures'}),
            'autopsy': forms.Select(attrs={'placeholder': 'Select Autopsy'}),
            'discharge_status': forms.Select(attrs={'placeholder': 'Select Discharge Status'}),
            'discharge_destination': forms.Select(attrs={'placeholder': 'Select Discharge Destination'}),
        }
        labels = {
            'discharge_date': 'Discharge Date',
            'discharge_time': 'Discharge Time',
            'length_of_stay': 'Length of Stay (days)',
            'final_diagnosis': 'Final Diagnosis',
            'associated_diagnosis': 'Associated Diagnosis',
            'service_type': 'Service Type',
            'operation_procedures': 'Operation Procedures',
            'autopsy': 'Autopsy',
            'discharge_status': 'Discharge Status',
            'discharge_destination': 'Discharge Destination',
        }
        help_texts = {
            'discharge_date': 'Enter discharge date in YYYY-MM-DD format',
            'discharge_time': 'Enter discharge time in HH:MM:SS format',
            'length_of_stay': 'Length of stay will be calculated automatically',
            'final_diagnosis': 'Enter final diagnosis',
            'associated_diagnosis': 'Enter associated diagnosis',
            'service_type': 'Select service type',
            'operation_procedures': 'Enter operation procedures',
            'autopsy': 'Select whether autopsy was performed',
            'discharge_status': 'Select discharge status',
            'discharge_destination': 'Select discharge destination',
        }
