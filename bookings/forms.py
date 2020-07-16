from django import forms
from datetime import datetime, timedelta
import datetime
from .models import Dependencies, RestrictedBookingDates, Appointment
class BookingForm(forms.Form):

    def get_dates(self):
        days=[('','')]
        day= datetime.datetime.now()+timedelta(0)
        day_to_add=day.weekday()

        # get valid dates that are not weekends
        while len(days)<4:
            
            if day_to_add == 5:
                day= day+timedelta(2)
                day_to_add=day.weekday()
            elif day_to_add == 6:
                day= day+timedelta(1)
                day_to_add=day.weekday()
            else:
                day=day+timedelta(1)
                day_to_add=day.weekday()
            if(day_to_add < 5):
                if RestrictedBookingDates.objects.filter(date_restricted=day.date()).exists()==False:
                    days.append((day.date(),day.date()))
        return tuple(days)

    def __init__(self,patientId=None,choices=[],*args, **kwargs):

        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['day_to_book'] = forms.ChoiceField(choices = self.get_dates,widget=forms.Select(attrs={"onChange":'refresh()'}))
        self.fields['book_time'] = forms.ChoiceField(choices = choices)
        self.fields['booked_for'] = forms.ModelChoiceField(queryset = Dependencies.objects.filter(patient_id=patientId), required=False)
        self.fields['symptoms']  = forms.CharField(label='Symptoms', max_length=400,
                                widget=forms.Textarea( ))


    def clean(self):
        cleaned_data= super().clean()
        date_to_book = self.cleaned_data.get('day_to_book')
        book_for = self.cleaned_data.get('booked_for')
        book_time = self.cleaned_data.get('book_time')
        booked = Appointment.objects.filter(appointment_date=date_to_book).filter(bookedfor=book_for).exists()
        slot_taken = Appointment.objects.filter(appointment_date=date_to_book).filter(bookedfor=book_time).exists()
        if booked==True:
            raise forms.ValidationError(f'{book_for} Already has a slot')
        if slot_taken==True:
            raise forms.ValidationError(f'{book_time} slot is taken please reload page and try another slot :)')
        if date_to_book is not None:
            pass
        else:
            raise forms.ValidationError("Please Select Booking date")

class RestrictDateForm(forms.Form):
    restrict_date = forms.DateField()

    def clean(self):
        clean_data= super().clean() 
        date = self.cleaned_data.get('restrict_date')
        if date<=datetime.datetime.now().date():
            raise forms.ValidationError("You can only restrict from tomorrow going forward")
        if date.weekday()==5 or date.weekday()==6:
            raise forms.ValidationError(f"{date.day} is a weekend")
        date_from_data = RestrictedBookingDates.objects.filter(date_restricted=date)
        if date_from_data.count()>0:
            raise forms.ValidationError("Date already in list")



class SearchForm(forms.Form):

    appointment_number = forms.CharField(label='Search Number',max_length=10, required=False)
    STATUS=( 
        ('Awaiting', 'Awaiting'),
        ('Completed', 'Completed')
    )
    status = forms.ChoiceField(choices=STATUS, required=False)
