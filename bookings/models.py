import datetime
from django.db import models


class MedicalAid(models.Model):
    board_name = models.CharField(max_length=200)
    contact_address = models.CharField(max_length=300)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.board_name
    


class Patient(models.Model):
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE, blank=True, null=True)
    medical_aid = models.ForeignKey(MedicalAid, on_delete=models.DO_NOTHING,  blank=True, null=True)
    medical_aid_number = models.CharField(verbose_name='medicalaid number', max_length=50, null=True, blank=True)
    def __str__(self):
        return f'{self.user.id}'
    


class Dependencies(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField(verbose_name="date of birth")
    date_of_registry = models.DateTimeField(verbose_name='date registry', auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    GENDER = (
        ("M", "MALE"),
        ("F", "FEMALE")
     )
    gender = models.CharField( choices=GENDER, default='M', max_length=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def age(self):
        return  datetime.date.today().year - self.date_of_birth.date().year


class Appointment(models.Model):
    STATUS = [
        ('Awaiting', 'Awaiting'),
        ('Completed', 'Completed')
    ]
    appointment_date = models.DateTimeField(verbose_name='appointment date')
    booked_on = models.DateTimeField(auto_now_add=True)
    booked_time = models.CharField(max_length=200)
    symptoms = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS, default='Awaiting')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bookedfor = models.CharField(max_length=400, default='willard', blank=True, null=True)
    appointment_number = models.CharField(max_length=4, default='0000', unique=True)

class RestrictedBookingDates(models.Model):
    date_restricted = models.DateTimeField(verbose_name='Restrict Date')

    def __str__(self):
        return f'{self.date_restricted.date()}'
    