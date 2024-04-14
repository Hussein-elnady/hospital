from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime, date

national_number_regex = RegexValidator(r"^\d{14}$", "National ID must be 14 digits")


class Patient(models.Model):
    national_number = models.CharField(max_length=14, unique=True, validators=[national_number_regex])
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')], null=True, blank=True)
    insurance_number = models.CharField(max_length=20, null=True, blank=True)
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
            today = date.today()
            age = today.year - year_of_birth - ((today.month, today.day) < (month_of_birth, day_of_birth))
            self.age = age
            gender = "male" if int(self.national_number[9:13]) % 2 != 0 else "female"
            return {
                "date_of_birth": date_of_birth,
                "gender": gender
            }
        return {}

    def save(self, *args, **kwargs):
        extracted_info = self.extract_national_id_info()
        if extracted_info:
            self.date_of_birth = extracted_info["date_of_birth"]
            self.gender = extracted_info["gender"]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Admission(models.Model):
    admission_number = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
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
    time_of_registration = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            last_admission = Admission.objects.order_by('-admission_number').first()
            if last_admission:
                last_admission_number = last_admission.admission_number
                if last_admission_number:
                    self.admission_number = last_admission_number + 1
                else:
                    self.admission_number = 1
            else:
                self.admission_number = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admission #{self.admission_number} for {self.patient.full_name}"


class Discharge(models.Model):
    admission_number = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge')
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

    def save(self, *args, **kwargs):
        if self.discharge_date is not None and self.discharge_time is not None:
            if self.admission_number.admission_date is not None and self.admission_number.admission_time is not None:
                admission_datetime = datetime.combine(self.admission_number.admission_date, self.admission_number.admission_time)
                discharge_datetime = datetime.combine(self.discharge_date, self.discharge_time)
                self.length_of_stay = (discharge_datetime - admission_datetime).days
            else:
                self.length_of_stay = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Discharge for {self.admission_number.patient.full_name}"
