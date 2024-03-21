from django.db import models
from lib.national_id import NationalID
from django.core.validators import RegexValidator
from datetime import date

national_number_regex = RegexValidator(r"^\d{14}$", "National ID must be 14 digits")


class Admission(models.Model):
    # Admission details
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)  # Link to Patient model
    full_name = models.CharField(max_length=255)  # Duplicate for convenience during admission
    date_of_birth = models.DateField(blank=True, null=True)  # In case info not available from national ID
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')])
    national_number = models.CharField(max_length=14, validators=[national_number_regex])
    insurance_number = models.CharField(max_length=20)
    admission_number = models.CharField(max_length=20, unique=True, editable=False)
    social_status = models.CharField(max_length=20,
                                     choices=[('single', 'أعزب'), ('married', 'متزوج'), ('divorced', 'مطلق'),
                                              ('widowed', 'أرمل')])
    religion = models.CharField(max_length=20,
                                choices=[('Muslim', 'مسلم'), ('Christian', 'مسيحي'), ('Other than that', 'غير ذلك')])
    profession = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city_village = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_relationship = models.CharField(max_length=255)
    emergency_contact_address = models.CharField(max_length=255)
    emergency_contact_phone_number = models.CharField(max_length=20)
    insurance_provider_contact_name = models.CharField(max_length=255)
    insurance_provider_relationship = models.CharField(max_length=255)
    insurance_provider_address = models.CharField(max_length=255)
    insurance_provider_phone_number = models.CharField(max_length=20)
    accident_location = models.CharField(max_length=20,
                                         choices=[('home', 'المنزل'), ('work', 'العمل'), ('road', 'الطريق'),
                                                  ('other', 'أخرى')])
    police_report = models.CharField(max_length=20, choices=[('Yes', 'نعم'), ('No', 'لا')])
    previous_admission = models.CharField(max_length=20, choices=[('Yes', 'نعم'), ('No', 'لا')])
    treating_physician = models.CharField(max_length=255)
    admission_department = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    room_grade = models.CharField(max_length=255)
    initial_diagnosis = models.TextField()
    service_type = models.CharField(max_length=20,
                                    choices=[('free', 'مجاني'), ('economic', 'اقتصادي'), ('insurance', 'تأمين'),
                                             ('government', 'نفقة دولة')])
    is_temporary = models.BooleanField(default=True)  # Flag for temporary admission data

    def calculate_length_of_stay(self):
        if self.discharge:
            return (self.discharge.discharge_date - self.admission_date).days
        return 0

    def save(self, *args, **kwargs):
        if not self.admission_number:
            today = date.today().strftime("%Y%m%d")
            admission_count = Admission.objects.filter(admission_number__startswith=today).count()
            serial_number = str(admission_count + 1).zfill(4)
            self.admission_number = f"{today}-{serial_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admission for {self.full_name}"


class Discharge(models.Model):
    discharge_id = models.AutoField(primary_key=True)
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE)
    # Discharge details
    discharge_date = models.DateField()
    final_diagnosis = models.TextField()
    autopsy = models.CharField(max_length=3, choices=[('yes', 'نعم'), ('No', 'لا')])
    discharge_status = models.CharField(max_length=20, choices=[('recovery', 'شفاء'), ('improvement', 'تحسن'),
                                                                ('no_improvement', 'لم تتحسن'), ('death', 'وفاة')])
    discharge_destination = models.CharField(max_length=20,
                                             choices=[('clinic', 'عيادة'), ('other_hospital', 'مستشفى أخرى'),
                                                      ('request', 'خروج حسب الطلب'), ('home', 'المنزل')])

    def __str__(self):
        return f"Discharge for Admission ID: {self.admission.id}"


class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')])
    national_number = models.CharField(max_length=14, validators=[national_number_regex], unique=True)
    insurance_number = models.CharField(max_length=20)
    admission_number = models.CharField(max_length=20)
    social_status = models.CharField(max_length=20,
                                     choices=[('single', 'أعزب'), ('married', 'متزوج'), ('divorced', 'مطلق'),
                                              ('widowed', 'أرمل')])
    religion = models.CharField(max_length=20,
                                choices=[('Muslim', 'مسلم'), ('Christian', 'مسيحي'), ('Other than that', 'غير ذلك')])
    profession = models.CharField(max_length=255)
    employer = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city_village = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_relationship = models.CharField(max_length=255)
    emergency_contact_address = models.CharField(max_length=255)
    emergency_contact_phone_number = models.CharField(max_length=20)
    insurance_provider_contact_name = models.CharField(max_length=255)
    insurance_provider_relationship = models.CharField(max_length=255)
    insurance_provider_address = models.CharField(max_length=255)
    insurance_provider_phone_number = models.CharField(max_length=20)
    current_admission = models.OneToOneField(
        Admission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_patient_admission',
        unique=True  # Add unique constraint
    )

    def fetch_info_from_national_id(self, national_id):
        instance = NationalID(national_id)
        try:
            success, info = instance.get_info()
            if success:
                self.date_of_birth = f"{info['year_of_birth']}-{info['month_of_birth']}-{info['day_of_birth']}"
                self.governorate = info['governorate']
                # You can extract and assign other fields similarly
                self.save()
                return True
            else:
                return False
        except Exception as e:
            # Handle exceptions gracefully
            print(f"An error occurred while fetching info from national ID: {e}")
            return False

    def save(self, *args, **kwargs):
        # Fetch information from national ID before saving if it's not already fetched
        if not self.date_of_birth or not self.governorate:
            self.fetch_info_from_national_id(self.national_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
