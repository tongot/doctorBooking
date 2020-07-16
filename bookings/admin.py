from django.contrib import admin
from account.models import Account
from bookings.models import (MedicalAid, Patient, Appointment)
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display= ('email', 'first_name', 'last_name','date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter =()
    fieldsets = ()
    add_fieldsets =()

admin.site.register(Account, AccountAdmin)
admin.site.register(MedicalAid)
admin.site.register(Patient)
admin.site.register(Appointment)
