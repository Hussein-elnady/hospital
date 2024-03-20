from django.db import models
from lib.national_id import NationalID
from django.core.validators import RegexValidator

national_number_regex = RegexValidator(r"^\d{14}$", "National ID must be 14 digits")


class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')])
    national_number = models.CharField(max_length=14, validators=[national_number_regex])
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
    admitted_by = models.CharField(max_length=20,
                                   choices=[('reception', 'استقبال'),
                                            ('clinic', 'عيادة'),
                                            ('other', 'أخرى')])
    accident_location = models.CharField(max_length=20,
                                         choices=[('home', 'المنزل'),
                                                  ('work', 'العمل'),
                                                  ('road', 'الطريق'),
                                                  ('other', 'أخرى')])
    police_report = models.CharField(max_length=20,
                                     choices=[('Yes', 'نعم'),
                                              ('No', 'لا'), ])
    previous_admission = models.CharField(max_length=20,
                                          choices=[('Yes', 'نعم'),
                                                   ('No', 'لا')])
    treating_physician = models.CharField(max_length=255)
    admission_department = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    room_grade = models.CharField(max_length=255)
    initial_diagnosis = models.TextField()
    admission_date = models.DateField()
    admission_time = models.TimeField()
    discharge_date = models.DateField()
    discharge_time = models.TimeField()
    length_of_stay = models.IntegerField()
    final_diagnosis = models.TextField()
    associated_diagnosis = models.TextField()
    service_type = models.CharField(max_length=20,
                                    choices=[('free', 'مجاني'), ('economic', 'اقتصادي'), ('insurance', 'تأمين'),
                                             ('government', 'نفقة دولة')])
    operation_procedures = models.TextField()
    autopsy = models.CharField(max_length=3, choices=[('yes', 'نعم'), ('No', 'لا')])
    discharge_status = models.CharField(max_length=20, choices=[('recovery', 'شفاء'), ('improvement', 'تحسن'),
                                                                ('no_improvement', 'لم تتحسن'), ('death', 'وفاة')])
    discharge_destination = models.CharField(max_length=20,
                                             choices=[('clinic', 'عيادة'), ('other_hospital', 'مستشفى أخرى'),
                                                      ('request', 'خروج حسب الطلب'), ('home', 'المنزل')])

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
