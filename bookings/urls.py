from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking),
    path('restrict_day', views.restrict_day),
    path('booking_list', views.booking_list),
    path('booking_list/<int:id>', views.change_status),
    path('booking_detail/<int:id>', views.delete_booking),
    path('cancel/<int:id>', views.cancel_booking),
    path('delete_date_restricted/<int:id>', views.delete_restricted_days),
    path('my_booking_list', views.my_booking_list)

]