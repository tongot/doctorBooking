from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm, RestrictDateForm, SearchForm
from .models import Patient, RestrictedBookingDates, Appointment
from django.core.mail import send_mail
import random


def send_email(book_number, time_booked, booker, date, email):
    send_mail('Hello from New Age',  
    f'Hi {booker},\n\nYour booking at {time_booked} no {date} has been reserved, you are expected to arrive 10 min before booked time.\n\nThank you',
    'newage@clinic.com',[email,], fail_silently=False,)

def randNumber():
    rand_number = random.randint(1000,9999)
    if Appointment.objects.filter(appointment_number=rand_number).count()>0:
        randNumber()
    else:
        return rand_number

def booking(request):
    if request.user.is_anonymous==False and request.user.is_admin==False:
        patient = get_object_or_404(Patient,user_id=request.user.id)
        BOOK_TIMES = [
            ('08:00:00','08:00:00'),
            ('08:30:00','08:30:00'),
            ('09:00:00','09:00:00'),
            ('09:30:00','09:30:00'),
            ('10:00:00','10:00:00'),
            ('10:30:00','10:30:00'),
            ('11:00:00','11:00:00'),
            ('11:30:00','11:30:00'),
            ('12:00:00','12:00:00'),
            ('12:30:00','12:30:00'),
            ('14:00:00','14:00:00'),
            ('14:30:00','14:30:00'),
            ('15:00:00','15:00:00'),
            ('15:30:00','15:30:00'),
            ('16:00:00','16:00:00')
        ]
        post_list=[]
        if request.method == 'POST':
            post_list.clear()
            booked = Appointment.objects.filter(appointment_date=request.POST['day_to_book'])
            if booked.count()>0:
                for book in booked:
                    BOOK_TIMES.remove((book.booked_time,book.booked_time))

            post_list=BOOK_TIMES
            form = BookingForm(patientId=patient.id, choices=post_list, data=request.POST)
            if form.is_valid():
                appointment_date = form.cleaned_data['day_to_book']
                booked_time = form.cleaned_data['book_time']
                symptoms = form.cleaned_data['symptoms']
                booked_for = form.cleaned_data['booked_for']

                rand= randNumber()

                appointment= Appointment(
                    appointment_date=appointment_date,
                    booked_time=booked_time,
                    symptoms=symptoms,
                    patient=patient,
                    bookedfor=booked_for,
                    appointment_number=rand
                )
               
                send_email(appointment.appointment_number,booked_time,request.user.full_name,appointment_date,request.user.email)
                appointment.save()

                return redirect('/my_booking_list/')
            else:
                return render(request, 'booking.htm', {'form':form})  
        else:
            form = BookingForm(patientId=patient.id)
            appointments =  Appointment.objects.filter(patient_id=patient.id)
            context = {
                'form':form,
                'appointments':appointments
            }
            return render(request, 'booking.htm', context)
    else:
        return redirect('/account/login')

def my_booking_list(request):
     if request.user.is_anonymous==False and request.user.is_admin==False:
        patient = get_object_or_404(Patient,user_id=request.user.id)
        appointments =  Appointment.objects.filter(patient_id=patient.id)
        context = {
            'appointments':appointments
        }
        return render(request, 'my_booking_list.htm', context)

def restrict_day(request):
    if request.user.is_anonymous==False:
        if request.method == 'POST':
            form = RestrictDateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['restrict_date']
                book_date = RestrictedBookingDates(date_restricted=date)
                book_date.save()
                return redirect('/booking/restrict_day')
            else:
                context={
                    'form':form
                }
                return render(request, 'restrict_date.htm', context)  
        else:
            form = RestrictDateForm()
            context = {
                'form':form,
                'disabled_dates':RestrictedBookingDates.objects.all()
            }
            return render(request, 'restrict_date.htm', context)
    else:
        return redirect('/account/login')
        
def booking_list(request):
    if request.user.is_anonymous==False:
        if request.user.is_admin==True:
            if request.method == 'POST':
                form = SearchForm(request.POST)
                data=[]
                appointment_number = request.POST['appointment_number']
                status= request.POST['status']
                if appointment_number == '' or appointment_number is None:
                    data = Appointment.objects.all()
                else:
                    data = Appointment.objects.filter(appointment_number=appointment_number).filter(status=status)
                context={
                    'form': form,
                    "booking_list":data
                }
                return render(request, 'booking_list.htm', context)
            else:
                form = SearchForm()
                context={
                    'form': form,
                    "booking_list": Appointment.objects.all()
                }
                return render(request, 'booking_list.htm', context)
        else:
           return redirect('/account/login')
    else:
       return redirect('/account/login')
   
def change_status(request,id=1):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "Completed"
    appointment.save()
    return redirect('/booking/booking_list')

def delete_booking(request,id=1):
    if request.method== "POST":
        Appointment.objects.filter(id=id).delete()
        return redirect('/booking/booking_list')
    else:
        to_delete = get_object_or_404(Appointment, id=id)
        context={
            'details': to_delete
        }
        return render(request, 'book_detail.htm', context)

def cancel_booking(request,id):
    if request.user.is_anonymous==False:
        if request.method== 'GET':
            appointment= get_object_or_404(Appointment, id=id)
            appointment.delete()
            return redirect('/booking')
    else:
        redirect('/account/login')
    
def delete_restricted_days(request,id):

    if request.user.is_anonymous==False:
        if request.user.is_admin==True:
            date = get_object_or_404(RestrictedBookingDates, id=id)
            date.delete()
            return redirect('/booking/restrict_day')
        else:
            return redirect('/account/login')
    else:
        return redirect('/account/login')