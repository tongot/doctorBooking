from django.shortcuts import render
from .models import WorkDone
from bookings.models import RestrictedBookingDates
import datetime

def index(request):
    dates=RestrictedBookingDates.objects.filter(date_restricted__gt=datetime.datetime.now())
    count=dates.count()
    context = {
        'data':WorkDone.objects.all(),
        'available_dates':dates,
        'count_of_dates':count
    }
    return render(request, 'index.htm', context)

def about(request):
    context = {}
    return render(request, 'AboutUs.htm', context)

def contact(request):
    context = {}
    return render(request, 'contact.htm', context)


