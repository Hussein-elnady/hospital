from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date

national_number_regex = RegexValidator(r"^\d{14}$", "National ID must be 14 digits")


# Define a custom validator for the national ID
def national_id_validator(value):
    if len(value) != 14:
        raise ValidationError("National ID must be 14 digits")
    # Extract components
    century = int(value[0])
    year_of_birth = int(value[1:3])
    month_of_birth = int(value[3:5])
    day_of_birth = int(value[5:7])


class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')], null=True, blank=True)
    national_number = models.CharField(max_length=14, validators=[national_number_regex], null=True, blank=True)
    insurance_number = models.CharField(max_length=20, null=True, blank=True)
    admission_number = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    social_status = models.CharField(max_length=20,
                                     choices=[('single', 'أعزب'), ('married', 'متزوج'), ('divorced', 'مطلق'),
                                              ('widowed', 'أرمل')], null=True, blank=True)
    religion = models.CharField(max_length=20,
                                choices=[('Muslim', 'مسلم'), ('Christian', 'مسيحي'), ('Other than that', 'غير ذلك')],
                                null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    employer = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city_village = models.CharField(max_length=255, null=True, blank=True)
    governorate = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_address = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone_number = models.CharField(max_length=20, null=True, blank=True)
    insurance_provider_contact_name = models.CharField(max_length=255, null=True, blank=True)
    insurance_provider_relationship = models.CharField(max_length=255, null=True, blank=True)
    insurance_provider_address = models.CharField(max_length=255, null=True, blank=True)
    insurance_provider_phone_number = models.CharField(max_length=20, null=True, blank=True)
    admitted_by = models.CharField(max_length=20,
                                   choices=[('reception', 'استقبال'),
                                            ('clinic', 'عيادة'),
                                            ('other', 'أخرى')], null=True, blank=True)
    accident_location = models.CharField(max_length=20,
                                         choices=[('home', 'المنزل'),
                                                  ('work', 'العمل'),
                                                  ('road', 'الطريق'),
                                                  ('other', 'أخرى')], null=True, blank=True)
    police_report = models.CharField(max_length=20,
                                     choices=[('Yes', 'نعم'),
                                              ('No', 'لا'), ], null=True, blank=True)
    previous_admission = models.CharField(max_length=20,
                                          choices=[('Yes', 'نعم'),
                                                   ('No', 'لا')], null=True, blank=True)
    treating_physician = models.CharField(max_length=255, null=True, blank=True)
    admission_department = models.CharField(max_length=255, null=True, blank=True)
    room = models.CharField(max_length=255, null=True, blank=True)
    room_grade = models.CharField(max_length=255, null=True, blank=True)
    initial_diagnosis = models.TextField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    admission_time = models.TimeField(null=True, blank=True)
    discharge_date = models.DateField(default=None)
    discharge_time = models.TimeField(default=None)
    length_of_stay = models.IntegerField(null=True, blank=True)
    final_diagnosis = models.TextField(null=True, blank=True)
    associated_diagnosis = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=20,
                                    choices=[('free', 'مجاني'), ('economic', 'اقتصادي'), ('insurance', 'تأمين'),
                                             ('government', 'نفقة دولة')], null=True, blank=True)
    operation_procedures = models.TextField(null=True, blank=True)
    autopsy = models.CharField(max_length=3, choices=[('yes', 'نعم'), ('No', 'لا')], null=True, blank=True)
    discharge_status = models.CharField(max_length=20,
                                        choices=[('recovery', 'شفاء'), ('improvement', 'تحسن'),
                                                 ('no_improvement', 'لم تتحسن'), ('death', 'وفاة')],
                                        null=True, blank=True)
    discharge_destination = models.CharField(max_length=20,
                                             choices=[('clinic', 'عيادة'), ('other_hospital', 'مستشفى أخرى'),
                                                      ('request', 'خروج حسب الطلب'), ('home', 'المنزل')],
                                             null=True, blank=True)
    time_of_registration = models.DateTimeField(auto_now_add=True)

    def extract_national_id_info(self):
        if self.national_number:
            century = int(self.national_number[0])
            year_of_birth = int(self.national_number[1:3])
            if century == 2:
                year_of_birth += 1900
            elif century == 3:
                year_of_birth += 2000
            month_of_birth = int(self.national_number[3:5])
            day_of_birth = int(self.national_number[5:7])
            date_of_birth = datetime(year_of_birth, month_of_birth, day_of_birth)
            # Calculate age based on date of birth
            today = date.today()
            age = today.year - year_of_birth - ((today.month, today.day) < (month_of_birth, day_of_birth))

            # Update the age field
            self.age = age

            gender = "male" if int(self.national_number[9:13]) % 2 != 0 else "female"
            return {
                "date_of_birth": date_of_birth,
                "gender": gender
            }
        return {}

    def save(self, *args, **kwargs):
        if not self.admission_number:  # Only generate if admission number is not set
            last_patient = Patient.objects.order_by('-admission_number').first()
            if last_patient:
                last_admission_number = last_patient.admission_number
                if last_admission_number:
                    serial_number = int(last_admission_number) + 1
                    self.admission_number = serial_number
                else:
                    self.admission_number = 1
            else:
                self.admission_number = 1

        # Calculate length_of_stay if discharge information is available
        if self.discharge_date and self.discharge_time and self.admission_date and self.admission_time:
            # Convert admission_date to datetime.date object
            admission_date_obj = datetime.strptime(self.admission_date, '%Y-%m-%d').date()
            # Convert admission_time to datetime.time object
            admission_time_obj = datetime.strptime(self.admission_time, '%H:%M').time()
            # Convert admission_time_obj to datetime.date object
            admission_time_obj = admission_time_obj.date()
            # Combine admission_date_obj and admission_time_obj
            admission_datetime = datetime.combine(admission_date_obj, admission_time_obj)
            # Convert discharge_date to datetime.date object
            discharge_date_obj = datetime.strptime(self.discharge_date, '%Y-%m-%d').date()
            # Convert discharge_time to datetime.time object
            discharge_time_obj = datetime.strptime(self.discharge_time, '%H:%M').time()
            # Combine discharge_date_obj and discharge_time_obj
            discharge_datetime = datetime.combine(discharge_date_obj, discharge_time_obj)
            # Calculate the difference in days
            length_of_stay = (discharge_datetime - admission_datetime).days
            self.length_of_stay = length_of_stay
        else:
            # If discharge information is not provided, set length_of_stay to None
            self.length_of_stay = None

        # Extract and update national ID information
        extracted_info = self.extract_national_id_info()
        if extracted_info:
            self.date_of_birth = extracted_info["date_of_birth"]
            self.gender = extracted_info["gender"]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Discharge(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    discharge_date = models.DateField(null=True, blank=True)
    discharge_time = models.TimeField(null=True, blank=True)
    length_of_stay = models.IntegerField(null=True, blank=True)
    final_diagnosis = models.TextField(null=True, blank=True)
    associated_diagnosis = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=20,
                                    choices=[('free', 'مجاني'), ('economic', 'اقتصادي'), ('insurance', 'تأمين'),
                                             ('government', 'نفقة دولة')], null=True, blank=True)
    operation_procedures = models.TextField(null=True, blank=True)
    autopsy = models.CharField(max_length=3, choices=[('yes', 'نعم'), ('No', 'لا')], null=True, blank=True)
    discharge_status = models.CharField(max_length=20,
                                        choices=[('recovery', 'شفاء'), ('improvement', 'تحسن'),
                                                 ('no_improvement', 'لم تتحسن'), ('death', 'وفاة')],
                                        null=True, blank=True)
    discharge_destination = models.CharField(max_length=20,
                                             choices=[('clinic', 'عيادة'), ('other_hospital', 'مستشفى أخرى'),
                                                      ('request', 'خروج حسب الطلب'), ('home', 'المنزل')],
                                             null=True, blank=True)

    def __str__(self):
        return self.patient.full_name
